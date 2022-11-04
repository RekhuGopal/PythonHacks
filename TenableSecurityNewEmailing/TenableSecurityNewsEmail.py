from datetime import date, datetime, timezone, timedelta
from newsapi import NewsApiClient
import boto3
from botocore.exceptions import ClientError
from json2html import *


class NewsMails:
    def __init__(self):
        client = boto3.resource('dynamodb', region_name="us-east-1")
        self.table = client.Table('AllEmails')
        self.NewsApikey = '2b8bbd66c2e2403692a4e778e0697c21'
        self.ses_client = boto3.client('ses',region_name="us-east-1")

    def getAllDynamoDBRecord (self):
        try :
            response = self.table.scan()
            emaildata = response['Items']
            while 'LastEvaluatedKey' in response:
                response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                emaildata.extend(response['Items'])
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Dynamo DB records returned , hence retruning now"),
            return emaildata

    def getAllNews (self , search) :
        try :
            print("get news for the  run...")
            newsapi = NewsApiClient(api_key= self.NewsApikey)
            from_date = datetime.now(timezone.utc) + timedelta(days=-3)
            end_time = datetime.now(timezone.utc) + timedelta(days=0)
            all_articles = newsapi.get_everything(q=search,from_param=from_date,to=end_time,language='en',sort_by='relevancy')
            print(all_articles)
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("News is retrieved as expected , hence retruning now"),
            return all_articles

    def Email_News(self , SourceEmail, ToEmail, finalresult):
        try:
            Sendresponse = self.ses_client.send_templated_email(
                                    Source=SourceEmail,
                                    Destination={
                                        'ToAddresses': [
                                            ToEmail
                                        ]
                                    },
                                    Template='NewAPIResultsMail',
                                    TemplateData= finalresult
                                )
        except Exception as e:
            print(str(e))
            return str(e)
        if Sendresponse['ResponseMetadata']['HTTPStatusCode'] == 200:
            print('email sent successfully..')
        else :
            print('email sending failed..')