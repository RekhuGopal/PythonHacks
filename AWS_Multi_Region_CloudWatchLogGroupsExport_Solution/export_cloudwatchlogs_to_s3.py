import boto3
import os
import datetime
import random
import time

def lambda_handler(event, context):
    log_group_name = event.get('logGroupName')
    print("logGroupName: ", log_group_name)
    region = event.get('region')
    print("region: ", region)
    
    if not log_group_name or not region:
        print("Error: 'logGroupName' and 'region' must be provided in the event.")
        return
    
    destination_bucket = "logexportbucketc"+region.replace("-", "").lower()
    ndays = 500
    
    current_time = datetime.datetime.now()
    start_date = current_time - datetime.timedelta(days=ndays)
    end_date = current_time - datetime.timedelta(days=ndays - 1)
    
    from_date = int(start_date.timestamp() * 1000)
    print("from_date: ", from_date)
    to_date = int(end_date.timestamp() * 1000)
    print("to_date: ", to_date)
    
    bucket_prefix = os.path.join(region, start_date.strftime('%Y/%m/%d'))
    response = create_export_task(log_group_name, from_date, to_date, destination_bucket, bucket_prefix, region)
    print(f"Created export task for log group: {log_group_name} in {region}, Response: {response}")

def create_export_task(log_group_name, from_time, to_time, destination_bucket, bucket_prefix, region):
    """Create an export task for the given CloudWatch log group with exponential backoff."""
    logs_client = boto3.client('logs', region_name=region)
    max_retries = 5
    base_delay = 1  # Base delay in seconds

    for attempt in range(max_retries):
        try:
            response = logs_client.create_export_task(
                logGroupName=log_group_name,
                fromTime=from_time,
                to=to_time,
                destination=destination_bucket,
                destinationPrefix=bucket_prefix
            )
            return response
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise  # Rethrow exception after max retries
            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)  # Exponential backoff with jitter
            time.sleep(delay)
