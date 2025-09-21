import boto3
import json
from botocore.config import Config

region = "us-west-2"
lambda_name = "invokevidegenai"

# Increase read timeout (e.g., 15 minutes)
config = Config(connect_timeout=60, read_timeout=900)  # 900 seconds = 15 minutes
lambda_client = boto3.client("lambda", region_name=region, config=config)

payload = {"prompt": "A cinematic dragon flying over mountains at sunset"}

response = lambda_client.invoke(
    FunctionName=lambda_name,
    InvocationType="RequestResponse",
    Payload=json.dumps(payload)
)

resp_payload = json.loads(response["Payload"].read().decode("utf-8"))
print("Status code:", resp_payload.get("statusCode"))
print("Response:", resp_payload)