import requests
import json

url = "http://localhost:8080/invocations"
headers = {
    "Content-Type": "application/json"
}
data = {
    "prompt": "Hello world!"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print("Status Code:", response.status_code)
print("Response:", response.text)