import logging
import boto3
from botocore.exceptions import ClientError
import os


## Create AWS S3 bucket using python boto3
def create_bucket(bucket_name, region=None):
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# Read the list of existing buckets
def list_bucket():
    # Create bucket
    try:
        s3 = boto3.client('s3')
        response = s3.list_buckets()
        if response:
            print('Buckets exists..')
            for bucket in response['Buckets']:
                print(f'  {bucket["Name"]}')
    except ClientError as e:
        logging.error(e)
        return False
    return True

# Upload a file from local system.
def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# Download a file from a S3 bucket.
def upload_file(file_name, bucket, object_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.download_file(bucket, object_name, file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# Delete a file from a S3 bucket.
def upload_file(bucket, key_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.delete_object(Bucket=bucket, Key=key_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# Delete bucket empty bucket
def delete_bucket(bucket, key_name):
    s3_client = boto3.client('s3')
    try:
        bucket = s3_client.Bucket(bucket)
        bucket.delete()
    except ClientError as e:
        logging.error(e)
        return False
    return True

list_bucket