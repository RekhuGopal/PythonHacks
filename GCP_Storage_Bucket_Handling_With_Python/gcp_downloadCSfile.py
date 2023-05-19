# import packages
from google.cloud import storage
import os

# set key credentials file path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'D:/VSCode/GitRepos/PythonHacks/GCP_Storage_Bucket_Handling_With_Python/cloudquicklabs-93d1e8c6ac6a.json'

# define function that downloads a file from the bucket
def download_cs_file(bucket_name, file_name, destination_file_name): 
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(file_name)
    blob.download_to_filename(destination_file_name)

    return True

download_cs_file('test_demo_storage_bucket', 'json/test.json', 'D:/VSCode/GitRepos/PythonHacks/GCP_Storage_Bucket_Handling_With_Python/download.json')