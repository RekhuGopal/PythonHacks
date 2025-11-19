import boto3
import json
import os
import argparse

client = boto3.client('bedrock-runtime')

parser = argparse.ArgumentParser()
parser.add_argument("--text", type=str, required=True, help="Prompt for text generation")
parser.add_argument("--modelid", type=str, required=True, help="Model ID for generation")
args = parser.parse_args()

prompt_data = args.text

body = json.dumps({"inputText": prompt_data})
modelId = args.modelid

accept = "application/json"
contentType = "application/json"

response = client.invoke_model(
    body=body, modelId=modelId, accept=accept, contentType=contentType
)
response_body = json.loads(response.get("body").read())

embedding = response_body.get("embedding")
print(embedding)
print(f"The embedding vector has {len(embedding)} values\n{embedding[0:5]+['...']+embedding[-3:]}")