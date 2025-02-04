import boto3
import json

def list_log_groups(region):
    """List all CloudWatch Log Groups in the specified region."""
    logs_client = boto3.client('logs', region_name=region)
    log_groups = []
    paginator = logs_client.get_paginator('describe_log_groups')
    
    for page in paginator.paginate():
        for log_group in page.get('logGroups', []):
            log_groups.append(log_group['logGroupName'])
    
    return log_groups

def invoke_lambda(log_group_name, lambda_function_name,lambda_region, source_region):
    """Invoke the specified AWS Lambda function with log group name as input."""
    lambda_client = boto3.client('lambda', region_name=lambda_region)
    event_payload = {
        "logGroupName": log_group_name,
        "region": source_region
    }
    response = lambda_client.invoke(
        FunctionName=lambda_function_name,
        InvocationType='Event',  # Async invocation
        Payload=json.dumps(event_payload)
    )
    return response

def lambda_handler(event, context):
    source_regions = ['ap-south-1', 'us-west-2', 'eu-west-1']  # List of AWS regions
    lambda_region = 'us-west-2'
    lambda_function_name = 'exporterlambda'  # Replace with your Lambda function name
    
    for source_region in source_regions:
        log_groups = list_log_groups(source_region)
        print(f"Found {len(log_groups)} log groups in {source_region}.")
        
        for log_group in log_groups:
            response = invoke_lambda(log_group, lambda_function_name, lambda_region, source_region)
            print(f"Invoked Lambda for log group: {log_group} in {source_region}, Response: {response['ResponseMetadata']['HTTPStatusCode']}")
