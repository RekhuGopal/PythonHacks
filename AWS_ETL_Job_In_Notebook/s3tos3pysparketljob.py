#Importing all the basic Glue, Spark libraries 

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

# Important further required libraries

from pyspark.sql.functions import udf, col
from pyspark.sql.types import IntegerType, StringType
from pyspark import SparkContext
from pyspark.sql import SQLContext
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

# leveraging the Country Code UDF

udf_get_country_code2 = udf(lambda z: get_country_code2(z), StringType())


# Reading the dataset into a DataFrame
s3_bucket = "s3://${BUCKET_NAME}/"                              # <------- PLEASE REPLACE ONLY THE ${BUCKET_NAME} HERE (Keep the "s3://" and the final "/" part)!!!
job_time_string = datetime.now().strftime("%Y%m%d%H%M%S")

df = spark.read.load(s3_bucket + "input/lab2/sample.csv", 
                     format="csv", 
                     sep=",", 
                     inferSchema="true", 
                     header="true")

# Performing a transformation that adds a new Country Code column to the dataframe based on the Country Code UDF output

new_df = df.withColumn('country_code_2', udf_get_country_code2(col("country")))
# Sinking the data into another S3 bucket path

new_df.write.csv(s3_bucket + "/output/lab3/notebook/" + job_time_string + "/")
job.commit()