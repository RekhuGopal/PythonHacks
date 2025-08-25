import boto3
import json

bedrock = boto3.client("bedrock", region_name="us-west-2")
response = bedrock.list_foundation_models(byCustomizationType="FINE_TUNING")
models = response.get("modelSummaries", [])

print("Available fine-tunable foundation models in us-west-2:\n")
for model in models:
    print("Model ID  :", model.get("modelId"))
    print("Model ARN :", model.get("modelArn"))
    print("-" * 60)
