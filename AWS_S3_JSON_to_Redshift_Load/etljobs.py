import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node DemoS3
DemoS3_node1708157626612 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={"paths": ["s3://databucketsourceside/"], "recurse": True},
    transformation_ctx="DemoS3_node1708157626612",
)

# Script generated for node Amazon Redshift
AmazonRedshift_node1708157811671 = glueContext.write_dynamic_frame.from_options(
    frame=DemoS3_node1708157626612,
    connection_type="redshift",
    connection_options={
        "postactions": "BEGIN; MERGE INTO public.jsontable USING public.jsontable_temp_p0uwrn ON jsontable.id = jsontable_temp_p0uwrn.id WHEN MATCHED THEN UPDATE SET id = jsontable_temp_p0uwrn.id, name = jsontable_temp_p0uwrn.name, city = jsontable_temp_p0uwrn.city, age = jsontable_temp_p0uwrn.age WHEN NOT MATCHED THEN INSERT VALUES (jsontable_temp_p0uwrn.id, jsontable_temp_p0uwrn.name, jsontable_temp_p0uwrn.city, jsontable_temp_p0uwrn.age); DROP TABLE public.jsontable_temp_p0uwrn; END;",
        "redshiftTmpDir": "s3://aws-glue-assets-357171621133-us-west-2/temporary/",
        "useConnectionProperties": "true",
        "dbtable": "public.jsontable_temp_p0uwrn",
        "connectionName": "Redshift connection",
        "preactions": "CREATE TABLE IF NOT EXISTS public.jsontable (id INTEGER, name VARCHAR, city VARCHAR, age INTEGER); DROP TABLE IF EXISTS public.jsontable_temp_p0uwrn; CREATE TABLE public.jsontable_temp_p0uwrn (id INTEGER, name VARCHAR, city VARCHAR, age INTEGER);",
    },
    transformation_ctx="AmazonRedshift_node1708157811671",
)

job.commit()
