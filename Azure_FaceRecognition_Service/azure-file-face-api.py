# import modules
import requests

# Request headers set Subscription key which provides access to this API. Found in your Cognitive Services accounts.
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '719c4b853f9f4d06ae435ade7d1c4cd2',
}

body = dict()
body["url"] = "http://www.imagozone.com/var/albums/vedete/Matthew%20Perry/Matthew%20Perry.jpg?m=1355670659"
body = str(body)

# Request URL 
FaceApiDetect = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=true&returnFaceAttributes=age,gender,headPose,smile,facialHair' 

try:
    # REST Call 
    response = requests.post(FaceApiDetect, data=body, headers=headers) 
    print("RESPONSE:" + str(response.json()))

except Exception as e:
    print(e)