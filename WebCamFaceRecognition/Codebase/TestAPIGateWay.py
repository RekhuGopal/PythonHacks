import requests
import io
from PIL import Image

#url = "https://v263zxf6m5.execute-api.us-west-2.amazonaws.com/v1/upload"
url2 = "https://v263zxf6m5.execute-api.us-west-2.amazonaws.com/v1/verify"


#image = Image.open(os.getcwd()+"/webcaptures/Y5DOKA9GXL.png")
image = Image.open("./webcaptures/20230521_125543.png")
stream = io.BytesIO()
image.save(stream,format="png")
image_binary = stream.getvalue()


headers = {
  'Content-Type': 'application/png',
  'x-api-key': 'GTUn6Fepnr8WWnLxYAT1c88HfWiRK7aN48qNyf0h'
}

response = requests.request("GET", url2, headers=headers, data=image_binary)

print(response.text)
