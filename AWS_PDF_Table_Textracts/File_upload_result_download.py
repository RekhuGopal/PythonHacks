import boto3
import logging
import os

# Get S3 bucket object tag
def get_s3_object_tag(bucket, object_name):
    s3_client = boto3.client('s3')
    try:
        get_tags_response = s3_client.get_object_tagging( Bucket=bucket, Key=object_name)
        if get_tags_response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Tag set are retrieved..")
            return get_tags_response['TagSet']
        else:
            print("Tag set are not retrieved..")
            return False
    except Exception as e:
        logging.error(e)
        return False

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


'''
## Upload a file to bucket
result_upload = upload_file("F:\\RekhuAll\\AzurePoC\\0C7A2552.JPG", bucket, object_name)
if result_upload :
    print("bucket file uploaded successfully..!")
else:
    print("bucket file upload failed..!")
'''

'''
## Get a file tag which is job id from bucket
result_get_tag = get_s3_object_tag(bucket, object_name)
if result_get_tag :
    print(result_get_tag)
    print("bucket file tags retrieved successfully..!")
else:
    print("bucket file tags retrieve failed..!")
'''

'''
## Download a file from bucket
result_download = download_file("F:\\RekhuAll\\AzurePoC\\0C7A2552.JPG", bucket, object_name)
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
