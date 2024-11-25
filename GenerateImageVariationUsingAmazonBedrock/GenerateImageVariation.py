# Use the native inference API to create an image with Titan Image Generator G1

import base64
import boto3
import json
import os
import random


def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            # Read the image and encode it to base64
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_image_variation(encodedImage):
    try: 
        # Create a Bedrock Runtime client in the AWS Region of your choice.
        client = boto3.client("bedrock-runtime", region_name="us-west-2")

        # Set the model ID, e.g., Titan Image Generator G1.
        model_id = "amazon.titan-image-generator-v1"

        # Define the image generation prompt for the model.
        prompt = "A dog sitting infront of bag"

        # Format the request payload using the model's native structure.
        native_request = {"imageVariationParams":{"images":[encodedImage],"text":prompt},"taskType":"IMAGE_VARIATION","imageGenerationConfig":{"cfgScale":8,"seed":0,"width":1024,"height":1024,"numberOfImages":3}}

        # Convert the native request to JSON.
        request = json.dumps(native_request)

        # Invoke the model with the request.
        response = client.invoke_model(modelId=model_id, body=request)

        # Decode the response body.
        model_response = json.loads(response["body"].read())

        # Extract the image data.
        base64_image_data = model_response["images"][0]

        # Save the generated image to a local folder.
        i, output_dir = 1, "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        while os.path.exists(os.path.join(output_dir, f"image_{i}.png")):
            i += 1

        image_data = base64.b64decode(base64_image_data)

        image_path = os.path.join(output_dir, f"image_{i}.png")
        with open(image_path, "wb") as file:
            file.write(image_data)

        print(f"The generated image has been saved to {image_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
image_path ="D:\VSCode\GitRepos\PythonHacks\GenerateImageVariationUsingAmazonBedrock\output\image_3.png"  
# Replace with your image path
encoded_image = image_to_base64(image_path)

if encoded_image:
    generate_image_variation(encoded_image)