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
Table = []

def PoliceData(policestrg):
    try:
        if 'NOT_SELECTED,' in policestrg :
            return policestrg.replace("NOT_SELECTED,", "")
        if 'Qualis' in policestrg :
            return policestrg.replace("Qualis", "")
        if 'Side Seite des Rades' in policestrg :
            return policestrg.replace("Side Seite des Rades", "")
        return policestrg
    except Exception as exception :
        print("Exception in GetTableFromTextractResult and error is {} ".format(exception))

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

def UploadResultToS3Bucket(jobId, data):
    try:
        print("Inside upload results to S3 bucket..")
        dynamicfilename = jobId +".json"
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

def GetFromTextractResult(pages):
    try:
        ConvertedToDictionary = json.loads(pages)
        doc = trp.Document(ConvertedToDictionary)
        i = 0
        for page in doc.pages:
            wagen_number = page.form.getFieldByKey('Wagennummer:')
            print(wagen_number.key.text)
            print(wagen_number.value.text)

            date_data = page.form.getFieldByKey('Datum')
            print(date_data.key.text)
            print(date_data.value.text)
            if str(wagen_number.value.text) and str(date_data.value.text):
                formdata = {}
                formdata[str(wagen_number.key.text)] = str(wagen_number.value.text)
                formdata[str(date_data.key.text)] = str(date_data.value.text)
                i +=1
        if i > 0:
            print("wagon number and date found")
            Table.append(formdata)
        return True
    except Exception as exception :
        print("Exception in GetTableFromTextractResult and error is {} ".format(exception))
        return False

def GetTableTextractResult(pages, jobId):
    try:
        ConvertedToDictionary = json.loads(pages)
        doc = trp.Document(ConvertedToDictionary)
        for page in doc.pages:
            for table in page.tables:
                if (page.tables).index(table) == 1:
                    for r, row in enumerate(table.rows):
                        if (table.rows).index(row) > 1:
                            i = 0
                            rowst = {}
                            for c, cell in enumerate(row.cells):
                                rowst[str((table.rows)[1].cells[i]).strip()] = PoliceData(str(cell)).strip()
                                i +=1
                            Table.append(rowst)
                    print(Table)
                    UploadResultToS3Bucket(jobId, Table)
        return True
    except Exception as exception :
        print("Exception in GetTableFromTextractResult and error is {} ".format(exception))
        return False

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
            if GetFromTextractResult(result) :
                print ("Date and wagonnumber added to list..")
                if GetTableTextractResult(result, qmessage['JobId']) :
                    print ("Process completed successfully..")
                else:
                    print ("Table data not retrieved..")
            else:
                print ("Date and wagonnumber retrieval failed..")
        else:
            print("results did not retrieved..")
    else:
        print("Job is not successfull..")
    
