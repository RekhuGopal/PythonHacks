import boto3
import logging
import os

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
    except Exception as e:
        logging.error(e)
        return False
    return True

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
    except Exception as e:
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
    except Exception as e:
        logging.error(e)
        return False
    return True

# Download a file from a S3 bucket.
def download_file(file_name, bucket, object_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.download_file(bucket, object_name, file_name)
    except Exception as e:
        logging.error(e)
        return False
    return True

# Delete a file from a S3 bucket.
def delete_file(bucket, key_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.delete_object(Bucket=bucket, Key=key_name)
    except Exception as e:
        logging.error(e)
        return False
    return True

# Delete bucket empty bucket
def delete_bucket(bucket):
    s3_client = boto3.client('s3')
    try:
        bucket = s3_client.delete_bucket(Bucket=bucket)
    except Exception as e:
        logging.error(e)
        return False
    return True

## Read list of buckets
'''
list_bucket()
'''

'''
## Calling Create Bucket
result_create = create_bucket("s3boto3test1")
if result_create :
    print("bucket got created successfully..!")
else:
    print("bucket got created failed..!")
'''


'''
## Upload a file to bucket
result_upload = upload_file("F:\\RekhuAll\\AzurePoC\\0C7A2552.JPG", "s3boto3test1", "0C7A2552.JPG")
if result_upload :
    print("bucket file uploaded successfully..!")
else:
    print("bucket file upload failed..!")
'''

'''
## Download a file from bucket
result_download = download_file("F:\\RekhuAll\\AzurePoC\\0C7A2552.JPG", "s3boto3test1", "0C7A2552.JPG")
if result_download :
    print("bucket file downloaded successfully..!")
else:
    print("bucket file download failed..!")
'''

'''
## Delete a file from bucket
result_delete = delete_file("s3boto3test1", "0C7A2552.JPG")
if result_delete :
    print("bucket file deleted successfully..!")
else:
    print("bucket file delete failed..!")
'''


## Delete bucket
result_deletebucket = delete_bucket("s3boto3test1")
if result_deletebucket :
    print("bucket deleted successfully..!")
else:
    print("bucket delete failed..!")
