import boto3
from botocore.exceptions import ClientError

## Change With Your Own Bucket
BUCKET_NAME = "glueworkshop-357171621133-us-west-2"
client = boto3.client('glue')

# Create database
try:
    response = client.create_database(
        DatabaseInput={
            'Name': 'python_glueworkshop',
            'Description': 'This database is created using Python boto3',
        }
    )
    print("Successfully created database")
except ClientError as e:
    print(f"error in creating database: {e.response['Error']['Code']} - {e.response['Error']['Message']}")

# Create Glue Crawler
try:
    response = client.create_crawler(
        Name='python-lab1',
        Role='AWSGlueServiceRole-glueworkshop',
        DatabaseName='python_glueworkshop',
        Targets={
            'S3Targets': [
                {
                    'Path': 's3://{BUCKET_NAME}/input/lab1/csv'.format(BUCKET_NAME=BUCKET_NAME),
                },
                {
                    'Path': 's3://{BUCKET_NAME}/input/lab5/json'.format(BUCKET_NAME=BUCKET_NAME),
                }
            ]
        },
        TablePrefix='python_'
    )
    print("Successfully created crawler")
except ClientError as e:
    print(f"error in creating crawler: {e.response['Error']['Code']} - {e.response['Error']['Message']}")

# This is the command to start the Crawler
try:
    response = client.start_crawler(
        Name='python-lab1'
    )
    print("Successfully started crawler")
except ClientError as e:
    print(f"error in starting crawler: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
