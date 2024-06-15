import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrameCollection
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame

# Script generated for node Aggregate Case Count
def AggregateCaseCount(glueContext, dfc) -> DynamicFrameCollection:
    df = dfc.select(list(dfc.keys())[0]).toDF()
    from pyspark.sql import functions as f

    df0 = df.groupBy("combinedname").agg({"positiveincrease": "sum", "totaltestresultsincrease": "sum"})
    dyf0 = DynamicFrame.fromDF(df0, glueContext, "result0")
    return DynamicFrameCollection({"CustomTransform0": dyf0}, glueContext)
# Script generated for node Multiple Output
def CreateMultipleOutput(glueContext, dfc) -> DynamicFrameCollection:
    df = dfc.select(list(dfc.keys())[0]).toDF()
    from pyspark.sql import functions as f

    df.createOrReplaceTempView("inputTable")
    df0 = spark.sql("SELECT TO_DATE(CAST(UNIX_TIMESTAMP(date, 'yyyyMMdd') AS TIMESTAMP)) as date, \
                            state , \
                            (positiveIncrease * 100 / totalTestResultsIncrease) as positivePercentage, \
                            StateName \
                    FROM inputTable ")

    df1 = df.withColumn('CombinedName', f.concat(f.col('StateName'), f.lit('('), f.col('state'), f.lit(')')))

    dyf0 = DynamicFrame.fromDF(df0, glueContext, "result0")
    dyf1 = DynamicFrame.fromDF(df1, glueContext, "result1")

    return DynamicFrameCollection({
                                    "CustomTransform0": dyf0, 
                                    "CustomTransform1": dyf1
                                    }, 
                                    glueContext)
def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node COVID data
COVIDdata_node1718468643082 = glueContext.create_dynamic_frame.from_catalog(database="console_glueworkshop", table_name="console_json", transformation_ctx="COVIDdata_node1718468643082")

# Script generated for node State Name
StateName_node1718468645661 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://glueworkshop-357171621133-us-west-2/input/lab5/state/states.csv"], "recurse": True}, transformation_ctx="StateName_node1718468645661")

# Script generated for node Join Data
SqlQuery623 = '''
SELECT  coviddata.date,
        coviddata.state,
        coviddata.positiveincrease,
        coviddata.totaltestresultsincrease,
        statename.StateName
FROM    coviddata LEFT JOIN statename
        ON  coviddata.state = statename.Code
WHERE   coviddata.state in ('NY', 'CA')
'''
JoinData_node1718468915820 = sparkSqlQuery(glueContext, query = SqlQuery623, mapping = {"statename":StateName_node1718468645661, "coviddata":COVIDdata_node1718468643082}, transformation_ctx = "JoinData_node1718468915820")

# Script generated for node Change Schema
ChangeSchema_node1718469195055 = ApplyMapping.apply(frame=JoinData_node1718468915820, mappings=[("date", "string", "date", "string"), ("state", "string", "state", "string"), ("positiveincrease", "double", "positiveincrease", "double"), ("totaltestresultsincrease", "double", "totaltestresultsincrease", "double"), ("StateName", "string", "StateName", "string")], transformation_ctx="ChangeSchema_node1718469195055")

# Script generated for node Multiple Output
MultipleOutput_node1718469391653 = CreateMultipleOutput(glueContext, DynamicFrameCollection({"ChangeSchema_node1718469195055": ChangeSchema_node1718469195055}, glueContext))

# Script generated for node Increase cases
Increasecases_node1718470520750 = SelectFromCollection.apply(dfc=MultipleOutput_node1718469391653, key=list(MultipleOutput_node1718469391653.keys())[1], transformation_ctx="Increasecases_node1718470520750")

# Script generated for node Positive Percentage
PositivePercentage_node1718469917017 = SelectFromCollection.apply(dfc=MultipleOutput_node1718469391653, key=list(MultipleOutput_node1718469391653.keys())[0], transformation_ctx="PositivePercentage_node1718469917017")

# Script generated for node Aggregate Case Count
AggregateCaseCount_node1718470698441 = AggregateCaseCount(glueContext, DynamicFrameCollection({"Increasecases_node1718470520750": Increasecases_node1718470520750}, glueContext))

# Script generated for node Pivot by State
SqlQuery624 = '''
SELECT  date, positivePercentageNY, positivePercentageCA
FROM    positivepercentage 
        pivot (avg(positivePercentage) as positivePercentage 
        for state in ('NY' as positivePercentageNY, 'CA' as positivePercentageCA))


'''
PivotbyState_node1718470025607 = sparkSqlQuery(glueContext, query = SqlQuery624, mapping = {"positivepercentage":PositivePercentage_node1718469917017}, transformation_ctx = "PivotbyState_node1718470025607")

# Script generated for node Aggregate result
Aggregateresult_node1718470982107 = SelectFromCollection.apply(dfc=AggregateCaseCount_node1718470698441, key=list(AggregateCaseCount_node1718470698441.keys())[0], transformation_ctx="Aggregateresult_node1718470982107")

# Script generated for node Amazon S3
AmazonS3_node1718470205666 = glueContext.write_dynamic_frame.from_options(frame=PivotbyState_node1718470025607, connection_type="s3", format="json", connection_options={"path": "s3://glueworkshop-357171621133-us-west-2/output/lab3/", "partitionKeys": []}, transformation_ctx="AmazonS3_node1718470205666")

# Script generated for node Amazon S3
AmazonS3_node1718471038471 = glueContext.write_dynamic_frame.from_options(frame=Aggregateresult_node1718470982107, connection_type="s3", format="json", connection_options={"path": "s3://glueworkshop-357171621133-us-west-2/output/lab3/", "compression": "snappy", "partitionKeys": []}, transformation_ctx="AmazonS3_node1718471038471")

job.commit()