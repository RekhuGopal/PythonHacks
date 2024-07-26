import boto3
import json
from botocore.exceptions import ClientError

def invoke_llama2(bedrock_runtime_client, prompt):
        try:
            body = {
                "prompt": prompt,
                "temperature": 0.5,
                "top_p": 0.9,
                "max_gen_len": 512,
            }

            ## Change Llama 3.1 model id from bedrock
            model_id = 'meta.llama3-8b-instruct-v1:0'
            response = bedrock_runtime_client.invoke_model(
                modelId=model_id, body=json.dumps(body)
            )

            response_body = json.loads(response["body"].read())
            completion = response_body["generation"]

            return completion

        except ClientError:
            print("Couldn't invoke Llama 3")
            raise

brt = boto3.client(service_name='bedrock-runtime')
result = invoke_llama2(brt, 'Explain Pythogorous Therom')
print(result)