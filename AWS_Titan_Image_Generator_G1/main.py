import boto3
import json
import base64
from PIL import Image 
from io import BytesIO

bedrock_runtime = boto3.client(service_name="bedrock-runtime")

# ImageGenerationConfig Options:
#   numberOfImages: Number of images to be generated
#   quality: Quality of generated images, can be standard or premium
#   height: Height of output image(s)
#   width: Width of output image(s)
#   cfgScale: Scale for classifier-free guidance
#   seed: The seed to use for reproducibility  

body = json.dumps(
    {
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {
            "text": "Amazon forest tiger", 
        },
        "imageGenerationConfig": {
            "numberOfImages": 2,   # Range: 1 to 5 
            "quality": "premium",  # Options: standard or premium
            "height": 768,         # Supported height list in the docs 
            "width": 1280,         # Supported width list in the docs
            "cfgScale": 7.5,       # Range: 1.0 (exclusive) to 10.0
            "seed": 42             # Range: 0 to 214783647
        }
    }
)

response = bedrock_runtime.invoke_model(
    body=body, 
    modelId="amazon.titan-image-generator-v1",
    accept="application/json", 
    contentType="application/json"
)

response_body = json.loads(response.get("body").read())
images = [Image.open(BytesIO(base64.b64decode(base64_image))) for base64_image in response_body.get("images")]

for img in images:
    img.show()