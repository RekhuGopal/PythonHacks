import requests

url = "<Gateway URL>"

datadict = {
 "id" : "5645654645y65",
 "body-json" : {
  "name": "max",
  "id": 2453243554,
  "place" : "NewYork"
 }
}

APIGatewayKey = "<API Gateway Key>"
headers = {
  'Content-Type': 'application/jsons',
  'x-api-key': APIGatewayKey
}

response = requests.request("POST", url, headers=headers, json=datadict)

print(response.text)