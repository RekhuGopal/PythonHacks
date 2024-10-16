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

# Script generated for node Oracle-RDS
OracleRDS_node1729065918531 = glueContext.create_dynamic_frame.from_options(
    connection_type = "oracle",
    connection_options = {
        "useConnectionProperties": "true",
        "dbtable": "employees",
        "connectionName": "Oracle connection",
    },
    transformation_ctx = "OracleRDS_node1729065918531"
)

# Script generated for node Amazon Redshift
AmazonRedshift_node1729066249106 = glueContext.write_dynamic_frame.from_options(frame=OracleRDS_node1729065918531, connection_type="redshift", connection_options={"postactions": "BEGIN; MERGE INTO public.employees USING public.employees_temp_rbvu78 ON employees.id = employees_temp_rbvu78.id WHEN MATCHED THEN UPDATE SET id = employees_temp_rbvu78.id, first_name = employees_temp_rbvu78.first_name, last_name = employees_temp_rbvu78.last_name, email = employees_temp_rbvu78.email, hire_date = employees_temp_rbvu78.hire_date, salary = employees_temp_rbvu78.salary WHEN NOT MATCHED THEN INSERT VALUES (employees_temp_rbvu78.id, employees_temp_rbvu78.first_name, employees_temp_rbvu78.last_name, employees_temp_rbvu78.email, employees_temp_rbvu78.hire_date, employees_temp_rbvu78.salary); DROP TABLE public.employees_temp_rbvu78; END;", "redshiftTmpDir": "s3://aws-glue-assets-357171621133-us-west-2/temporary/", "useConnectionProperties": "true", "dbtable": "public.employees_temp_rbvu78", "connectionName": "Redshift connection", "preactions": "CREATE TABLE IF NOT EXISTS public.employees (id DECIMAL, first_name VARCHAR, last_name VARCHAR, email VARCHAR, hire_date TIMESTAMP, salary DECIMAL); DROP TABLE IF EXISTS public.employees_temp_rbvu78; CREATE TABLE public.employees_temp_rbvu78 (id DECIMAL, first_name VARCHAR, last_name VARCHAR, email VARCHAR, hire_date TIMESTAMP, salary DECIMAL);"}, transformation_ctx="AmazonRedshift_node1729066249106")

job.commit()