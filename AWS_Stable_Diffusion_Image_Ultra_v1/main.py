import base64
import io
import json
import logging
import boto3
from PIL import Image
from botocore.exceptions import ClientError

class ImageError(Exception):
    "Custom exception for errors returned by SDXL"
    def __init__(self, message):
        self.message = message


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def generate_image(model_id, body):
    try:
        logger.info("Generating image with SDXL model %s", model_id)

        bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')
    
        accept = "application/json"
        content_type = "application/json"

        # Send the request to invoke the model
        response = bedrock.invoke_model(
            modelId=model_id,
            contentType=content_type,
            accept=accept,
            body=body
        )

        # Read and decode the response body from the StreamingBody
        response_body = json.loads(response['body'].read().decode('utf-8'))

        # Decode the base64 image data
        image_bytes = base64.b64decode(response_body['images'][0])

        logger.info("Successfully generated image with SDXL model %s", model_id)

        return image_bytes
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        return False


def main():
    """
    Entrypoint for SDXL example.
    """

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")

    model_id = 'stability.stable-image-ultra-v1:0'

    prompt = "A kitten eating mcdonald burger"

    body = json.dumps({
        "prompt": prompt,
        "mode": "text-to-image",
        "aspect_ratio": "1:1",
        "output_format": "jpeg"
    })

    try:
        # Generate the image
        image_bytes = generate_image(model_id=model_id, body=body)

        # Convert bytes to an image and show it
        image = Image.open(io.BytesIO(image_bytes))
        image.show()

        # Optionally, save the image
        image.save('./generated_image.jpeg', 'JPEG')

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occurred: " + message)
    except ImageError as err:
        logger.error(err.message)
        print(err.message)
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        print(f"An unexpected error occurred: {err}")

    else:
        print(f"Finished generating text with SDXL model {model_id}.")


if __name__ == "__main__":
    main()
