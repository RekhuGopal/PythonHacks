import boto3
import json

bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')

modelId = 'amazon.titan-text-lite-v1'
accept = 'application/json'
contentType = 'application/json'
body = json.dumps({
    "inputText": "write a letter to my boss asking leave for a day",
    "textGenerationConfig":{
        "maxTokenCount":512,
        "stopSequences":[],
        "temperature":0,
        "topP":0.9
        }
})

response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

response_body = json.loads(response.get('body').read())
outputText = response_body.get('results')[0].get('outputText')

text = outputText[outputText.index('\n')+1:]
content = text.strip()
print(outputText)