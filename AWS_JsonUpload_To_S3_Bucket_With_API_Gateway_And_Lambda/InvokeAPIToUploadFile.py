import requests

url = "https://hhy0xsskr8.execute-api.us-west-2.amazonaws.com/v1/UploadJson"

image_binary = {
 "id" : "5645654645y65",
 "body-json" : {
  "name": "refgdfgf",
  "id": 24534,
  "place" : "bng"
 }
}

APIGatewayKey = "GTUn6Fepnr8WWnLxYAT1c88HfWiRK7aN48qNyf0h"
headers = {
  'Content-Type': 'application/png',
  'x-api-key': APIGatewayKey
}

response = requests.request("POST", url, headers=headers, json=image_binary)

print(response.text)