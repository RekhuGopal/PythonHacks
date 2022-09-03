import boto3
import json
import sys
import time
import urllib.parse

sqs = boto3.client('sqs' , region_name='us-east-1')
sns = boto3.client('sns', region_name='us-east-1')

def DeleteTopicandQueue(sqsQueueUrl, snsTopicArn):
        sqs.delete_queue(QueueUrl=sqsQueueUrl)
        sns.delete_topic(TopicArn=snsTopicArn)

def CreateTopicandQueue():
    
    millis = str(int(round(time.time() * 1000)))

    # Create SNS topic
    snsTopicName = "AmazonTextractTopic" + millis
    topicResponse = sns.create_topic(Name=snsTopicName)
    snsTopicArn = topicResponse['TopicArn']

    # create SQS queue
    sqsQueueName = "AmazonTextractQueue" + millis
    sqs.create_queue(QueueName=sqsQueueName)
    sqsQueueUrl = sqs.get_queue_url(QueueName=sqsQueueName)['QueueUrl']
    attribs = sqs.get_queue_attributes(QueueUrl=sqsQueueUrl,AttributeNames=['QueueArn'])['Attributes']
    sqsQueueArn = attribs['QueueArn']

    # Subscribe SQS queue to SNS topic
    sns.subscribe(TopicArn=snsTopicArn,Protocol='sqs',Endpoint=sqsQueueArn)

    # Authorize SNS to write SQS queue
    policy = """{{
                    "Version":"2012-10-17",
                    "Statement":[
                        {{
                        "Sid":"MyPolicy",
                        "Effect":"Allow",
                        "Principal" : {{"AWS" : "*"}},
                        "Action":"SQS:SendMessage",
                        "Resource": "{}",
                        "Condition":{{
                            "ArnEquals":{{
                            "aws:SourceArn": "{}"
                            }}
                        }}
                        }}
                    ]
                    }}""".format(sqsQueueArn, snsTopicArn)

    response = sqs.set_queue_attributes(QueueUrl=sqsQueueUrl,Attributes={'Policy': policy})

    return snsTopicArn , sqsQueueUrl

result = CreateTopicandQueue()
if result:
   print("SNS ARN is :", result)