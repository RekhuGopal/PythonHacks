import boto3
from decimal import Decimal
import json
import urllib

print('Loading function')

dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

def index_faces(bucket, key):

    response = rekognition.index_faces(
        Image={"S3Object":
            {"Bucket": bucket,
            "Name": key}},
            CollectionId="100Collections")
    return response
    
def update_index(tableName,faceId,firstName,laststName,DOB,Phonenumber):
    response = dynamodb.put_item(
        TableName=tableName,
        Item={
            'FaceId': {'S': faceId},
            'FirstName': {'S': firstName},
            'LastName': {'S': laststName},
            'DOB': {'S': DOB},
            'Phonenumber': {'S': Phonenumber}
            }
        ) 
    return True


def lambda_handler(event, context):
    
    print(event)

    try:
        response = index_faces(event['bucket'], event['key'])
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            faceId = response['FaceRecords'][0]['Face']['FaceId']
            print(faceId)
            firstName = event['firstName']
            laststName = event['lastName']
            DOB = event['dob']
            Phonenumber = event['phoneNumber']
            if update_index('FaceRecords',faceId,firstName,laststName,DOB,Phonenumber):
                print("run complete")
                return {
                    'statusCode': 200,
                    'message' :  "Face Recorded successfully"
                    }
            else:
                print("run failed to complete")
                return {
                    'statusCode': 404,
                    'message' :  "Face Record Creation Failed"
                    }
        
    except Exception as e:
        print("Error in face record creation {}".format(e))
        return {
                    'statusCode': 404,
                    'message' :  "Face Record Creation Failed"
                }