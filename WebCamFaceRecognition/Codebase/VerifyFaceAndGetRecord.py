import json
import base64
import boto3
import string
import random

s3 = boto3.client("s3")
rekognition = boto3.client('rekognition', region_name='us-west-2')
dynamodb = boto3.client('dynamodb', region_name='us-west-2')

def lambda_handler(event, context):
    try:
        get_file_content = event["body-json"]
        decode_content = base64.b64decode(get_file_content)
        pic_filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        s3_upload = s3.put_object(Bucket="verifyfiles-to-s3-bucket",Key=pic_filename+".png",Body=decode_content)
        print("Upload is succes ", s3_upload)
        if s3_upload['ResponseMetadata']['HTTPStatusCode'] == 200 :
            keyname = pic_filename+".png"
            response = rekognition.search_faces_by_image(
                CollectionId='100Collections',
                Image={
                        'S3Object': {
                            'Bucket': "verifyfiles-to-s3-bucket",
                            'Name': keyname
                        } 
                    }                                  
                )
            MatchList = []
            if 'FaceMatches'in response:
                print("matches found, now gathering data..")
                for match in response['FaceMatches']:
                    facedata = {}
                    facedata['Confidence'] = match['Face']['Confidence']
                    facedata['FaceId'] = match['Face']['FaceId']
                    MatchList.append(facedata)
                print(MatchList)
            
            if len(MatchList) != 0:
                for match in MatchList:
                    print("iterating match found : ", match)
                    print (match['FaceId'], match['Confidence'])
                    face = dynamodb.get_item (
                            TableName='FaceRecords',  
                            Key={'FaceId': {'S': match['FaceId']}}
                           )
                    print("Dynamo Search result..", face)
                    if 'Item' in face:
                        print ("The face match returned..!!")
                        return {
                            'statusCode': 200,
                            'firstName': face['Item']['FirstName']['S'],
                            'lastName': face['Item']['LastName']['S'],
                            'dob': face['Item']['DOB']['S'],
                            'phoneNumber': face['Item']['Phonenumber']['S'],
                            'matchconfidence': round(match['Confidence'], 2)
                        }
            else:
                print ('no match found from Rekognition service..!!')
                return {
                        'statusCode': 404,
                        'Message': "No match found in Rekognition service"
                    }
        print("Upload failed or no records found in Rekognition service")        
        return {
                'statusCode': 404,
                'Message': "No records found for the face..!!"
           }
    except Exception as e:
        print("Error in processing face verification {}".format(e))
        return {
                'statusCode': 404,
                'Message': "Error occured while verifying face in Rekognition service"
            }