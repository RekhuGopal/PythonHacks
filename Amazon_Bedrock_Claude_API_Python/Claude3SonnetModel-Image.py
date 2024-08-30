import boto3
import json
import base64

# Create a Bedrock Runtime client in the AWS Region of your choice.
client = boto3.client("bedrock-runtime", region_name="us-west-2")

# Function to encode image to base64
def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
        base64_encoded_data = base64.b64encode(image_data)
        return base64_encoded_data.decode('utf-8')

# Set the model ID
model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

# Define the prompt
prompt = "What's in this image?"

# Encode the image
encoded_image = encode_image_to_base64("./dog.jpg")

# Format the request payload
payload = {
    "modelId": model_id,
    "body": json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": encoded_image
                        }
                    }
                ]
            }
        ]
    }),
    "contentType": "application/json",
    "accept": "application/json"
}

# Invoke the model
try:
    response = client.invoke_model(
        modelId=model_id,
        body=payload['body'],
        contentType=payload['contentType'],
        accept=payload['accept']
    )
    
    # Attempt to read and print the response body
    if 'body' in response:
        response_body = response['body'].read().decode('utf-8')
        print(response_body)
    else:
        print("Response does not contain 'Body' key. Check the response object for details.")

except Exception as e:
    print(f"An error occurred: {e}")
