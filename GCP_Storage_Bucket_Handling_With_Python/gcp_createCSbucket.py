# import packages
from google.cloud import storage
import os

# set key credentials file path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'D:/VSCode/GitRepos/PythonHacks/GCP_Storage_Bucket_Handling_With_Python/cloudquicklabs-93d1e8c6ac6a.json'

# define function that creates the bucket
def create_bucket(bucket_name, storage_class='STANDARD', location='us-central1'): 
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = storage_class
   
    bucket = storage_client.create_bucket(bucket, location=location) 
    # for dual-location buckets add data_locations=[region_1, region_2]
    
    return f'Bucket {bucket.name} successfully created.'

## Invoke Function
print(create_bucket('test_demo_storage_bucket', 'STANDARD', 'us-central1'))