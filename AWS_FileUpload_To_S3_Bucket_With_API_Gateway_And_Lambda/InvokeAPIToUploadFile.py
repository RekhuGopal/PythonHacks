import requests
import io
from PIL import Image
import os

url = "<Your API Gateway URL with Resource value>"


#image = Image.open(os.getcwd()+"/webcaptures/Y5DOKA9GXL.png")
image = Image.open("./webcaptures/010.png")
stream = io.BytesIO()
image.save(stream,format="PNG")
image_binary = stream.getvalue()

APIGatewayKey = "<Your API Gateway Key>"
headers = {
  'Content-Type': 'application/png',
  'x-api-key': APIGatewayKey
}

response = requests.request("POST", url, headers=headers, data=image_binary)

print(response.text)
