import requests
import boto3
import datetime


sts_client = boto3.client('sts')
t = datetime.datetime.utcnow()
amzdate = t.strftime('%Y%m%dT%H%M%SZ')
print(amzdate)
datestamp = t.strftime('%Y%m%d')
print(datestamp)
region = 'us-east-1'
service =  'lambda'

def get_temp_sts_tokens():
    try:
        response = sts_client.get_session_token( DurationSeconds=900)
    except Exception as e:
        print("error occured and error is {}".format(e))
    else:
        return response
      
def invoke_lambda_url(sts_response):
    try:
        url = "https://qgisnbicde2dypkpqajhzjt3we0ofjhr.lambda-url.us-east-1.on.aws/"
        payload = ""
        headers = {
            'X-Amz-Security-Token': sts_response['Credentials']['SessionToken'],
            'X-Amz-Date': amzdate,
            'Authorization': 'AWS4-HMAC-SHA256 Credential='+sts_response['Credentials']['SecretAccessKey']+'/'+datestamp+'/'+region+'/'+service+'/aws4_request, SignedHeaders=host;x-amz-date;x-amz-security-token, Signature=5a14f99afde7b60336fec24b2383000f634a7338ae4b476035db1c8d07645672'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception as e:
        print("error occured while invoking lambda and error is {}".format(e))
    else:
         return response

sts_tkn = get_temp_sts_tokens()
print(sts_tkn)
result =  invoke_lambda_url(sts_tkn)
if result:
 print("results retrived is at below..")
 print(result.text)

