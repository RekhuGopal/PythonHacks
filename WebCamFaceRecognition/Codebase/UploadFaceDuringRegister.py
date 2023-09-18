import json
import base64
import boto3
import string
import random


def lambda_handler(event, context):
    try :
        s3 = boto3.client("s3")
        get_file_content = event["body-json"]
        decode_content = base64.b64decode(get_file_content)
        pic_filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        final_pic_filename = pic_filename+".png"
        s3_upload = s3.put_object(Bucket="uploadfiles-to-s3-bucket",Key=final_pic_filename,Body=decode_content)
        if s3_upload['ResponseMetadata']['HTTPStatusCode'] == 200 :
            print(" register image uploaded successfully..")
            return {
                'statusCode': 200,
                'keyname': final_pic_filename
        
            }
        else:
            print("Error in register face file upload {}".format(e))
            return {
                        'statusCode': 404,
                        'keyname': "NA"
                    }
            
    except Exception as e:
        print("Error in register face file upload {}".format(e))
        return {
                    'statusCode': 404,
                    'keyname': "NA"
                }