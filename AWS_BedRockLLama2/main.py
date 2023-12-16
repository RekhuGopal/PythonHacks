import boto3
import json
from botocore.exceptions import ClientError

def invoke_llama2(bedrock_runtime_client, prompt):
        """
        Invokes the Meta Llama 2 large-language model to run an inference
        using the input provided in the request body.

        :param prompt: The prompt that you want Jurassic-2 to complete.
        :return: Inference response from the model.
        """

        try:
            # The different model providers have individual request and response formats.
            # For the format, ranges, and default values for Meta Llama 2 Chat, refer to:
            # https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-meta.html

            body = {
                "prompt": prompt,
                "temperature": 0.5,
                "top_p": 0.9,
                "max_gen_len": 512,
            }

            # model_id = 'meta.llama2-13b-chat-v1'
            model_id = 'meta.llama2-70b-chat-v1'
            response = bedrock_runtime_client.invoke_model(
                modelId=model_id, body=json.dumps(body)
            )

            response_body = json.loads(response["body"].read())
            completion = response_body["generation"]

            return completion

        except ClientError:
            print("Couldn't invoke Llama 2")
            raise

# management plane, use bedrock
# brt = boto3.client(service_name='bedrock')
# brt.list_foundation_models()
brt = boto3.client(service_name='bedrock-runtime')
result = invoke_llama2(brt, 'how does rain?')
print(result)