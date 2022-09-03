from logging import exception
import boto3
import time
import json
from botocore.exceptions import ClientError

textract = boto3.client('textract', region_name='us-east-1')

def GetResults(jobId):
        maxResults = 1000
        paginationToken = None
        finished = False
        pages = []

        while finished == False:
            response = None
            if paginationToken == None:
                response = textract.get_document_analysis(JobId=jobId,MaxResults=maxResults)
            else:
                response = textract.get_document_analysis(JobId=jobId,MaxResults=maxResults,NextToken=paginationToken)
            pages.append(response)
            print('Document Detected.')
            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True
        pages = json.dumps(pages)
        return pages

def GetTableFromTextractResult(pages):
    ConvertedToDictionary = json.loads(pages)
    listOfBlock = ConvertedToDictionary[0]['Blocks']
    table_item = next((item for item in listOfBlock if item['BlockType'] == "TABLE" and "MERGED_CELL" in item['Relationships']), None)
    print("Table item is:  ", table_item)

def lambda_handler(event, context):
    print("event collected from sqs is : {}".format(event))
    print("required eventbody is:", event['Records'][0]['body'])
    modifiedEvent = json.loads(event['Records'][0]['body'])
    qmessage = json.loads(modifiedEvent['Message'])
    print("Job ID: ",qmessage['JobId'])
    print("Job status is : ",qmessage['Status'])
    if qmessage['Status'] == "SUCCEEDED" and qmessage['JobId'] :
        result = GetResults(qmessage['JobId'])
        if result:
            GetTableFromTextractResult(result)
        else:
            print("results did not retrieved..")
    else:
        print("Job is not successfull..")
    
