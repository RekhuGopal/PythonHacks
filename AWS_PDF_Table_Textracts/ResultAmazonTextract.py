from logging import exception
from operator import contains
import boto3
import json
from botocore.exceptions import ClientError
import trp

textract = boto3.client('textract', region_name='us-east-1')
jobId  = "157b0dcae9b5888113265018a8f4ed06a5d6e64c1747f102ca103f1e313f3a72"
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

def GetTableFromTextractResult(pages, jobId):
    try:
        ConvertedToDictionary = json.loads(pages)
        doc = trp.Document(ConvertedToDictionary)
        for page in doc.pages:
            for table in page.tables:
                print((page.tables).index(table))
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
                    #UploadResultToS3Bucket(jobId, (page.tables).index(table), Table)
    except Exception as exception :
        print("Exception in GetTableFromTextractResult and error is {} ".format(exception))

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

result = GetResults(jobId)
'''
if result:
    GetTableFromTextractResult(result, jobId)
else:
    print("results did not retrieved..")
'''

if result:
    if(GetFromTextractResult(result)):
        GetTableFromTextractResult(result, jobId)
else:
    print("results did not retrieved..")
    
