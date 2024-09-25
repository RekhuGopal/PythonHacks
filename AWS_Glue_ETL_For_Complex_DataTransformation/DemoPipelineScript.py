import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrameCollection
from awsglue.dynamicframe import DynamicFrame
import re

# Script generated for node Remove Records with NULL
def MyTransform(glueContext, dfc) -> DynamicFrameCollection:
    df = dfc.select(list(dfc.keys())[0]).toDF().na.drop()
    results = DynamicFrame.fromDF(df, glueContext, "results")
    return DynamicFrameCollection({"results": results}, glueContext)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Dropoff Zone Lookup
DropoffZoneLookup_node1727249077962 = glueContext.create_dynamic_frame.from_catalog(database="default", table_name="taxi_zone_lookup", transformation_ctx="DropoffZoneLookup_node1727249077962")

# Script generated for node Yellow Trip Data
YellowTripData_node1727246110049 = glueContext.create_dynamic_frame.from_catalog(database="default", table_name="yellow_tripdata", transformation_ctx="YellowTripData_node1727246110049")

# Script generated for node Pickup Zone Lookup
PickupZoneLookup_node1727248406668 = glueContext.create_dynamic_frame.from_catalog(database="default", table_name="taxi_zone_lookup", transformation_ctx="PickupZoneLookup_node1727248406668")

# Script generated for node Change Schema - Dropoff Zone Lookup
ChangeSchemaDropoffZoneLookup_node1727249128429 = ApplyMapping.apply(frame=DropoffZoneLookup_node1727249077962, mappings=[("locationid", "long", "do_location_id", "long"), ("borough", "string", "do_borough", "string"), ("zone", "string", "do_zone", "string"), ("service_zone", "string", "do_service_zone", "string")], transformation_ctx="ChangeSchemaDropoffZoneLookup_node1727249128429")

# Script generated for node Remove Records with NULL
RemoveRecordswithNULL_node1727246692033 = MyTransform(glueContext, DynamicFrameCollection({"YellowTripData_node1727246110049": YellowTripData_node1727246110049}, glueContext))

# Script generated for node Change Schema - Pickup Zone Lookup
ChangeSchemaPickupZoneLookup_node1727248471362 = ApplyMapping.apply(frame=PickupZoneLookup_node1727248406668, mappings=[("locationid", "long", "pu_location_id", "long"), ("borough", "string", "pu_borough", "string"), ("zone", "string", "pu_zone", "string"), ("service_zone", "string", "pu_service_zone", "string")], transformation_ctx="ChangeSchemaPickupZoneLookup_node1727248471362")

# Script generated for node SelectFromCollection
SelectFromCollection_node1727246788353 = SelectFromCollection.apply(dfc=RemoveRecordswithNULL_node1727246692033, key=list(RemoveRecordswithNULL_node1727246692033.keys())[0], transformation_ctx="SelectFromCollection_node1727246788353")

# Script generated for node Filter - Yellow Trip Data
FilterYellowTripData_node1727247328286 = Filter.apply(frame=SelectFromCollection_node1727246788353, f=lambda row: (bool(re.match("^2020-1", row["tpep_pickup_datetime"]))), transformation_ctx="FilterYellowTripData_node1727247328286")

# Script generated for node Yellow Trips Data + Pickup Zone Lookup
YellowTripsDataPickupZoneLookup_node1727248695311 = Join.apply(frame1=ChangeSchemaPickupZoneLookup_node1727248471362, frame2=FilterYellowTripData_node1727247328286, keys1=["pu_location_id"], keys2=["pulocationid"], transformation_ctx="YellowTripsDataPickupZoneLookup_node1727248695311")

# Script generated for node Yellow Trips Data + Pickup Zone Lookup + Dropoff Zone Lookup
YellowTripsDataPickupZoneLookupDropoffZoneLookup_node1727249210426 = Join.apply(frame1=ChangeSchemaDropoffZoneLookup_node1727249128429, frame2=YellowTripsDataPickupZoneLookup_node1727248695311, keys1=["do_location_id"], keys2=["dolocationid"], transformation_ctx="YellowTripsDataPickupZoneLookupDropoffZoneLookup_node1727249210426")

# Script generated for node Change Schema - Joined Data
ChangeSchemaJoinedData_node1727249404013 = ApplyMapping.apply(frame=YellowTripsDataPickupZoneLookupDropoffZoneLookup_node1727249210426, mappings=[("do_location_id", "long", "do_location_id", "long"), ("do_borough", "string", "do_borough", "string"), ("do_zone", "string", "do_zone", "string"), ("do_service_zone", "string", "do_service_zone", "string"), ("pu_location_id", "long", "pu_location_id", "long"), ("pu_borough", "string", "pu_borough", "string"), ("pu_zone", "string", "pu_zone", "string"), ("pu_service_zone", "string", "pu_service_zone", "string"), ("vendorid", "bigint", "vendorid", "long"), ("tpep_pickup_datetime", "string", "pickup_datetime", "timestamp"), ("tpep_dropoff_datetime", "string", "dropoff_datetime", "timestamp"), ("passenger_count", "bigint", "passenger_count", "long"), ("trip_distance", "double", "trip_distance", "double"), ("ratecodeid", "bigint", "ratecodeid", "long"), ("store_and_fwd_flag", "string", "store_and_fwd_flag", "string"), ("pulocationid", "bigint", "pulocationid", "long"), ("dolocationid", "bigint", "dolocationid", "long"), ("payment_type", "bigint", "payment_type", "long"), ("fare_amount", "double", "fare_amount", "double"), ("extra", "double", "extra", "double"), ("mta_tax", "double", "mta_tax", "double"), ("tip_amount", "double", "tip_amount", "double"), ("tolls_amount", "double", "tolls_amount", "double"), ("improvement_surcharge", "double", "improvement_surcharge", "double"), ("total_amount", "double", "total_amount", "double"), ("congestion_surcharge", "double", "congestion_surcharge", "double")], transformation_ctx="ChangeSchemaJoinedData_node1727249404013")

# Script generated for node Transformed Yellow Trip Data
TransformedYellowTripData_node1727249704198 = glueContext.write_dynamic_frame.from_options(frame=ChangeSchemaJoinedData_node1727249404013, connection_type="s3", format="glueparquet", connection_options={"path": "s3://serverlessanalytics-357171621133-transformed/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="TransformedYellowTripData_node1727249704198")

job.commit()