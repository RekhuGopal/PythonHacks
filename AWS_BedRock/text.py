import boto3
import json
import base64

client = boto3.client('bedrock-runtime')

# Specify the input data and model ID
input_data = {
  "modelId": "ai21.j2-mid-v1",
  "contentType": "application/json",
  "accept": "*/*",
  "body": "{\"prompt\":\"how to cook tomato rice\",\"maxTokens\":200,\"temperature\":0.7,\"topP\":1,\"stopSequences\":[],\"countPenalty\":{\"scale\":0},\"presencePenalty\":{\"scale\":0},\"frequencyPenalty\":{\"scale\":0}}"
}
"""

input_data = {
  "modelId": "cohere.command-text-v14",
  "contentType": "application/json",
  "accept": "*/*",
  "body": "{\"prompt\":\"how to cook tomato rice\",\"max_tokens\":4000,\"temperature\":0.75,\"p\":0.01,\"k\":0,\"stop_sequences\":[],\"return_likelihoods\":\"NONE\"}"
}
"""
# Invoke the model for inference
response = client.invoke_model(contentType='application/json', body=input_data['body'], modelId=input_data['modelId'])

Data = json.loads(response['body'].read().decode('utf-8'))

print(Data)
#Retrieve the inference response
print(Data['completions'][0]['data']['text'])
#print(Data['generations'][0]['text'])

