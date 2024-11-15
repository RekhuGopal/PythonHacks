import boto3
import json
# Create a Boto3 client for Bedrock Runtime

client = boto3.client('bedrock-runtime')

# Specify the input data and model ID
input_data = {
  "modelId": "stability.stable-diffusion-xl-v1",
  "contentType": "application/json",
  "accept": "application/json",
   "body": {"text_prompts":[{"text":"Sri lanka tea plantation."}],"cfg_scale":10,"seed":0,"steps":50}
}

# Invoke the model for inference
response = client.invoke_model(contentType='application/json', body=json.dumps(input_data["body"]).encode('utf-8'), modelId=input_data['modelId'])

# Retrieve the inference response
inference_result = response['body'].read().decode('utf-8')

print(inference_result)
