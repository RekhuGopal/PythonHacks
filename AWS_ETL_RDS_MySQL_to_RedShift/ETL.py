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

# Script generated for node Relational DB
RelationalDB_node1728549197468 = glueContext.create_dynamic_frame.from_options(
    connection_type = "mysql",
    connection_options = {
        "useConnectionProperties": "true",
        "dbtable": "test.employees",
        "connectionName": "Mysql connection",
    },
    transformation_ctx = "RelationalDB_node1728549197468"
)

# Script generated for node Amazon Redshift
AmazonRedshift_node1728549323270 = glueContext.write_dynamic_frame.from_options(frame=RelationalDB_node1728549197468, connection_type="redshift", connection_options={"postactions": "BEGIN; MERGE INTO public.employees USING public.employees_temp_pl71y8 ON employees.id = employees_temp_pl71y8.id WHEN MATCHED THEN UPDATE SET id = employees_temp_pl71y8.id, first_name = employees_temp_pl71y8.first_name, last_name = employees_temp_pl71y8.last_name, email = employees_temp_pl71y8.email, hire_date = employees_temp_pl71y8.hire_date, salary = employees_temp_pl71y8.salary WHEN NOT MATCHED THEN INSERT VALUES (employees_temp_pl71y8.id, employees_temp_pl71y8.first_name, employees_temp_pl71y8.last_name, employees_temp_pl71y8.email, employees_temp_pl71y8.hire_date, employees_temp_pl71y8.salary); DROP TABLE public.employees_temp_pl71y8; END;", "redshiftTmpDir": "s3://aws-glue-assets-357171621133-us-west-2/temporary/", "useConnectionProperties": "true", "dbtable": "public.employees_temp_pl71y8", "connectionName": "Redshift connection", "preactions": "CREATE TABLE IF NOT EXISTS public.employees (id INTEGER, first_name VARCHAR, last_name VARCHAR, email VARCHAR, hire_date DATE, salary DECIMAL); DROP TABLE IF EXISTS public.employees_temp_pl71y8; CREATE TABLE public.employees_temp_pl71y8 (id INTEGER, first_name VARCHAR, last_name VARCHAR, email VARCHAR, hire_date DATE, salary DECIMAL);"}, transformation_ctx="AmazonRedshift_node1728549323270")

job.commit()