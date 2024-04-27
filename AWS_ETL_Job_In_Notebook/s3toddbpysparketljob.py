#Importing all the basic Glue, Spark libraries 

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Important further required libraries

import os, sys, boto3
from pprint import pprint
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import udf, col
from pyspark.sql.types import IntegerType, StringType
from datetime import datetime

# Starting Spark/Glue Context

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# Important pycountry_convert function from the external python library (pycountry_convert.zip)

from pycountry_convert import (
    convert_country_alpha2_to_country_name,
    convert_country_alpha2_to_continent,
    convert_country_name_to_country_alpha2,
    convert_country_alpha3_to_country_alpha2,
)

# Defining the function code

def get_country_code2(country_name):
    country_code2 = 'US'
    try:
        country_code2 = convert_country_name_to_country_alpha2(country_name)
    except KeyError:
        country_code2 = ''
    return country_code2

udf_get_country_code2 = udf(lambda z: get_country_code2(z), StringType())

#Get parameter values

s3_bucket_name = "s3://${BUCKET_NAME}/"                              # <------- PLEASE REPLACE ONLY THE ${BUCKET_NAME} HERE (Keep the "s3://" and the final "/" part)!!!
region_name = '${AWS_REGION}'                                        #  <--- REPLACE THE AWS REGION
ddb_table_name='glueworkshop-lab3'


# Create the dynamodb with appropriate read and write capacity
# Get service resource
dynamodb = boto3.resource('dynamodb', region_name=region_name)

table_status = dynamodb.create_table(
    TableName=ddb_table_name,
    KeySchema=[{'AttributeName': 'uuid','KeyType': 'HASH'}],
    AttributeDefinitions=[{'AttributeName': 'uuid','AttributeType': 'N'}],
    ProvisionedThroughput={'ReadCapacityUnits': 500,'WriteCapacityUnits': 5000}
    )
# Wait until the table exists.
table_status.meta.client.get_waiter('table_exists').wait(TableName=ddb_table_name)
pprint(table_status)

df = spark.read.load(s3_bucket_name + "input/lab2/sample.csv", 
                     format="csv", 
                     sep=",", 
                     inferSchema="true", 
                     header="true")


new_df = df.withColumn('country_code_2', udf_get_country_code2(col("Country")))
new_df_dyf=DynamicFrame.fromDF(new_df, glueContext, "new_df_dyf")

print("Start writing to DBB : {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
glueContext.write_dynamic_frame_from_options(
    frame=new_df_dyf,
    connection_type="dynamodb",
    connection_options={
        "dynamodb.output.tableName": ddb_table_name,
        "dynamodb.throughput.write.percent": "1.0"
    }
)
print("Finished writing to DBB : {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

# Comparing Counts
    
new_df.count()


job.commit()