import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Amazon S3
AmazonS3_node1731780536224 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://databucketsourceside2/files/"], "recurse": True}, transformation_ctx="AmazonS3_node1731780536224")

# Script generated for node Amazon Redshift
AmazonRedshift_node1731780714421 = glueContext.write_dynamic_frame.from_options(frame=AmazonS3_node1731780536224, connection_type="redshift", connection_options={"postactions": "BEGIN; MERGE INTO public.employees USING public.employees_temp_atga6u ON employees.id = employees_temp_atga6u.id WHEN MATCHED THEN UPDATE SET id = employees_temp_atga6u.id, first_name = employees_temp_atga6u.first_name, last_name = employees_temp_atga6u.last_name, email = employees_temp_atga6u.email, hire_date = employees_temp_atga6u.hire_date, salary = employees_temp_atga6u.salary WHEN NOT MATCHED THEN INSERT VALUES (employees_temp_atga6u.id, employees_temp_atga6u.first_name, employees_temp_atga6u.last_name, employees_temp_atga6u.email, employees_temp_atga6u.hire_date, employees_temp_atga6u.salary); DROP TABLE public.employees_temp_atga6u; END;", "redshiftTmpDir": "s3://aws-glue-assets-357171621133-us-west-2/temporary/", "useConnectionProperties": "true", "dbtable": "public.employees_temp_atga6u", "connectionName": "Redshift connection", "preactions": "CREATE TABLE IF NOT EXISTS public.employees (id VARCHAR, first_name VARCHAR, last_name VARCHAR, email VARCHAR, hire_date VARCHAR, salary VARCHAR); DROP TABLE IF EXISTS public.employees_temp_atga6u; CREATE TABLE public.employees_temp_atga6u (id VARCHAR, first_name VARCHAR, last_name VARCHAR, email VARCHAR, hire_date VARCHAR, salary VARCHAR);"}, transformation_ctx="AmazonRedshift_node1731780714421")

job.commit()