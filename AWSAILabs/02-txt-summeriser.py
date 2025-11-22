import boto3
import json
import os
import argparse
import logging
from botocore.exceptions import ClientError

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

client = boto3.client('bedrock-runtime')

parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str, required=True, help="Prompt for text generation")
parser.add_argument("--modelid", type=str, required=True, help="Model ID for generation")
args = parser.parse_args()

modelId = args.modelid
accept = 'application/json'
contentType = 'application/json'

# Read the prompt from a text file
with open(args.file, "r") as file:
    prompt_data = file.read().strip()

# Format the prompt to start with "Human:" and end with "Assistant:"
formatted_prompt = f'Human: Please provide a summary of the following text in one small paragraph. {prompt_data} \n\nAssistant:'

messages = [{
    "role": "user",
    "content": [{"text": formatted_prompt}]
}]

# System prompts for Claude models
if modelId.startswith("anthropic"):
    system_prompts = [{"text": "You are an assistant that helps with various tasks. Provide clear and concise answers."}]
else:
    system_prompts = []

try:
    response = client.converse(
        modelId=modelId,
        messages=messages,
        system=system_prompts,
        inferenceConfig={"temperature": 0.5}
    )

    output_message = response['output']['message']
    output_text = "".join([content['text'] for content in output_message['content']])
    
    # Log token usage
    token_usage = response['usage']
    logger.info("Input tokens: %s", token_usage['inputTokens'])
    logger.info("Output tokens: %s", token_usage['outputTokens'])
    logger.info("Total tokens: %s", token_usage['totalTokens'])

    print(output_text)

except ClientError as err:
    message = err.response['Error']['Message']
    logger.error("A client error occurred: %s", message)
    print(f"A client error occurred: {message}")