from logging import exception
import boto3
import time
from botocore.exceptions import ClientError

SNSTopicArn = "arn:aws:sns:us-east-1:357171621133:AmazonTextractTopic1662190593066"
roleArn = "arn:aws:iam::357171621133:role/AWS_PDF_Table_Textract_Role"
textract = boto3.client('textract', region_name='us-east-1')

def ProcessDocument(s3_bucket, s3_key):
    sleepy_time = 1
    retry = 0
    flag = 'False'
    try:
        while retry < 4 and  flag == 'False' :
            response = textract.start_document_analysis(DocumentLocation={'S3Object': {'Bucket': s3_bucket, 'Name': s3_key}},
                                                FeatureTypes=["TABLES"],
                                                NotificationChannel={'RoleArn': roleArn, 'SNSTopicArn': SNSTopicArn})
            print(response)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print('Start Job Id: ' + response['JobId'])
                flag == 'True'
                return response['JobId']
            else:
                time_to_sleep = 2**retry
                retry +=1
                time.sleep(time_to_sleep)
    except Exception as exception :
        print("Exception happend message is: ", exception)
        return False
def lambda_handler(event, context):
    print("event collected is {}".format(event))
    record = event['Records'][0]
    s3_bucket = record['s3']['bucket']['name']
    print("Bucket name is {}".format(s3_bucket))
    s3_key = record['s3']['object']['key']
    print("Bucket key name is {}".format(s3_key))
    from_path = "s3://{}/{}".format(s3_bucket, s3_key)
    print("from path {}".format(from_path))
    TextractResult = ProcessDocument(s3_bucket, s3_key)
    if TextractResult :
        print("job id returned..") 
        return TextractResult
    else:
        return False
