import boto3
import json
import os

client = boto3.client('bedrock')

# Extract model IDs and join them with commas
model_data = client.list_foundation_models()
model_ids = [model['modelId'] for model in model_data['modelSummaries']]
print("Available models:")
print("")
print('\n'.join(model_ids))