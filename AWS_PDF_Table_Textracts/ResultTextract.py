from logging import exception
import boto3
import time
import json
from botocore.exceptions import ClientError
import trp
import os

textract = boto3.client('textract', region_name='us-east-1')
s3_client = boto3.resource('s3', region_name='us-east-1')
Bucket_name = "textractresultsd"

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

def UploadResultToS3Bucket(jobId, tableIndex, data):
    try:
        print("Inside upload results to S3 bucket..")
        dynamicfilename = jobId +"_"+str(tableIndex)+".json"
        print("Dynamic file name is :", dynamicfilename)
        local_file_path = "/tmp/textractresult.json"
        with open(local_file_path, 'w') as fp:
            json.dump(data, fp)
        print("Result is stored in local .json file..")
        s3_client.meta.client.upload_file(local_file_path, Bucket_name, dynamicfilename)
        print("file uploaded successfully..")
        os.remove(local_file_path)
        print("file deleted after upload to s3..")
    except Exception as exception :
        print("Exception in upload to s3 bucket and error is {} ".format(exception))

def GetTableFromTextractResult(pages, jobId):
    try:
        ConvertedToDictionary = json.loads(pages)
        doc = trp.Document(ConvertedToDictionary)
        for page in doc.pages:
            for table in page.tables:
                print((page.tables).index(table))
                Table = []
                for r, row in enumerate(table.rows):
                    i = 0
                    rowst = {}
                    for c, cell in enumerate(row.cells):
                        rowst[str((table.rows)[0].cells[i])] = str(cell)
                        i +=1
                    Table.append(rowst)
                print(Table)
                UploadResultToS3Bucket(jobId, (page.tables).index(table), Table)
    except Exception as exception :
        print("Exception in GetTableFromTextractResult and error is {} ".format(exception))

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
            GetTableFromTextractResult(result, qmessage['JobId'])
        else:
            print("results did not retrieved..")
    else:
        print("Job is not successfull..")
    
