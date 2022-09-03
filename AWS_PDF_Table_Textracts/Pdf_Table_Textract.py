import boto3
import json
import sys
import time
import urllib.parse

class ProcessType:
    DETECTION = 1
    ANALYSIS = 2


class DocumentProcessor:
    jobId = ''
    textract = boto3.client('textract')
    sqs = boto3.client('sqs')
    sns = boto3.client('sns')

    roleArn = ''
    bucket = ''
    document = ''

    sqsQueueUrl = ''
    snsTopicArn = ''
    processType = ''

    def main(self, bucketName, documentName):
        self.roleArn = '<past iam arn here>'

        self.bucket = bucketName
        self.document = documentName

        self.CreateTopicandQueue()
        self.ProcessDocument(ProcessType.ANALYSIS)
        self.DeleteTopicandQueue()

    def ProcessDocument(self, type):
        jobFound = False

        self.processType = type
        validType = False

        # Determine which type of processing to perform
        if self.processType == ProcessType.DETECTION:
            response = self.textract.start_document_text_detection(DocumentLocation={'S3Object': {'Bucket': self.bucket, 'Name': self.document}},
                                                                   NotificationChannel={'RoleArn': self.roleArn, 'SNSTopicArn': self.snsTopicArn})
            print('Processing type: Detection')
            validType = True

        if self.processType == ProcessType.ANALYSIS:
            response = self.textract.start_document_analysis(DocumentLocation={'S3Object': {'Bucket': self.bucket, 'Name': self.document}},
                                                             FeatureTypes=[
                                                                 "TABLES"],
                                                             NotificationChannel={'RoleArn': self.roleArn, 'SNSTopicArn': self.snsTopicArn})
            print('Processing type: Analysis')
            validType = True

        if validType == False:
            print("Invalid processing type. Choose Detection or Analysis.")
            return

        print('Start Job Id: ' + response['JobId'])
        dotLine = 0
        while jobFound == False:
            sqsResponse = self.sqs.receive_message(QueueUrl=self.sqsQueueUrl, MessageAttributeNames=['ALL'],
                                                   MaxNumberOfMessages=10)

            if sqsResponse:

                if 'Messages' not in sqsResponse:
                    if dotLine < 40:
                        print('.', end='')
                        dotLine = dotLine+1
                    else:
                        print()
                        dotLine = 0
                    sys.stdout.flush()
                    time.sleep(5)
                    continue

                for message in sqsResponse['Messages']:
                    notification = json.loads(message['Body'])
                    textMessage = json.loads(notification['Message'])
                    print(textMessage['JobId'])
                    print(textMessage['Status'])
                    if str(textMessage['JobId']) == response['JobId']:
                        print('Matching Job Found:' + textMessage['JobId'])
                        jobFound = True
                        results = self.GetResults(textMessage['JobId'])
                        self.StoreInS3(results)
                        self.sqs.delete_message(QueueUrl=self.sqsQueueUrl,
                                                ReceiptHandle=message['ReceiptHandle'])
                    else:
                        print("Job didn't match:" +
                              str(textMessage['JobId']) + ' : ' + str(response['JobId']))
                    # Delete the unknown message. Consider sending to dead letter queue
                    self.sqs.delete_message(QueueUrl=self.sqsQueueUrl,
                                            ReceiptHandle=message['ReceiptHandle'])

        print('Done!')

    # Store the result in a S3 bucket
    def StoreInS3(self, response):
        print('registering in s3 bucket...')
        outputInJsonText = str(response)
        pdfTextExtractionS3ObjectName = self.document.replace('.pdf', '')
        pdfTextExtractionS3Bucket = self.bucket

        s3 = boto3.client('s3')

        outputFileName = pdfTextExtractionS3ObjectName + '.json'
        s3.put_object(Body=outputInJsonText,
                      Bucket=pdfTextExtractionS3Bucket, Key=outputFileName)
        print('file ' + outputFileName + ' registered successfully!')

    def CreateTopicandQueue(self):

        millis = str(int(round(time.time() * 1000)))

        # Create SNS topic
        snsTopicName = "AmazonTextractTopic" + millis

        topicResponse = self.sns.create_topic(Name=snsTopicName)
        self.snsTopicArn = topicResponse['TopicArn']

        # create SQS queue
        sqsQueueName = "AmazonTextractQueue" + millis
        self.sqs.create_queue(QueueName=sqsQueueName)
        self.sqsQueueUrl = self.sqs.get_queue_url(
            QueueName=sqsQueueName)['QueueUrl']

        attribs = self.sqs.get_queue_attributes(QueueUrl=self.sqsQueueUrl,
                                                AttributeNames=['QueueArn'])['Attributes']

        sqsQueueArn = attribs['QueueArn']

        # Subscribe SQS queue to SNS topic
        self.sns.subscribe(
            TopicArn=self.snsTopicArn,
            Protocol='sqs',
            Endpoint=sqsQueueArn)

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
}}""".format(sqsQueueArn, self.snsTopicArn)

        response = self.sqs.set_queue_attributes(
            QueueUrl=self.sqsQueueUrl,
            Attributes={
                'Policy': policy
            })

    def DeleteTopicandQueue(self):
        self.sqs.delete_queue(QueueUrl=self.sqsQueueUrl)
        self.sns.delete_topic(TopicArn=self.snsTopicArn)

    def GetResults(self, jobId):
        maxResults = 1000
        paginationToken = None
        finished = False
        pages = []

        while finished == False:

            response = None

            if self.processType == ProcessType.ANALYSIS:
                if paginationToken == None:
                    response = self.textract.get_document_analysis(JobId=jobId,
                                                                   MaxResults=maxResults)
                else:
                    response = self.textract.get_document_analysis(JobId=jobId,
                                                                   MaxResults=maxResults,
                                                                   NextToken=paginationToken)

            if self.processType == ProcessType.DETECTION:
                if paginationToken == None:
                    response = self.textract.get_document_text_detection(JobId=jobId,
                                                                         MaxResults=maxResults)
                else:
                    response = self.textract.get_document_text_detection(JobId=jobId,
                                                                         MaxResults=maxResults,
                                                                         NextToken=paginationToken)

            # Put response on pages list
            pages.append(response)
            print('Document Detected.')

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True

        # convert pages as JSON pattern
        pages = json.dumps(pages)
        return pages


def lambda_handler(event, context):
    analyzer = DocumentProcessor()
    
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        analyzer.main(bucket, key)
        
        return 'Processing Done!'

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e