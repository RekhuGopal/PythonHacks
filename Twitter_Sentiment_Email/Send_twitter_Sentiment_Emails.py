import boto3
import json
import requests
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from datetime import date, datetime, timezone, timedelta

class NewsMails:
    def __init__(self):
        client = boto3.resource('dynamodb', region_name="us-east-1")
        self.ses_client = boto3.client('ses', region_name="us-east-1")
        self.table = client.Table('NewSubscribers')

    def GetAllDynamoDBRecord(self):
        try:
            response = self.table.scan()
            emaildata = response['Items']
            while 'LastEvaluatedKey' in response:
                response = self.table.scan(
                    ExclusiveStartKey=response['LastEvaluatedKey'])
                emaildata.extend(response['Items'])
        except ClientError as e:
            print(e.response['Error']['Message'])
            # Email_Failed_Transaction("Exception error while getting all DynamoDB records..!")
        else:
            print("Dynamo DB records returned , hence returning now"),
            return emaildata

    def gettwitter(self, brand, Email, UserName):
        try:
            bearer_token = 'AAAAAAAAAAAAAAAAAAAAAM%2BJhgEAAAAA78%2BfDj64ysNy%2BSH9kceIY6f9flk%3D67lVBv8oJFGteq01ZkOkBz9SyZh5V9PGbdzEM3e8w3jhRGYRFA'
            headers = {"Authorization": "Bearer {}".format(bearer_token)}
            url = "https://api.twitter.com/2/tweets/search/recent"
            query_params = {'query': brand,
                            # 'start_time': start_date,
                            # 'end_time': end_date,
                            'max_results': 10,
                            'tweet.fields': 'id,text,author_id,conversation_id,created_at,geo,lang,public_metrics,referenced_tweets',
                            'user.fields': 'id,name,username,created_at,description,location,public_metrics,verified',
                            'place.fields': 'full_name,id,country,country_code,geo,name,place_type'}
            response = requests.get(url, headers=headers, params=query_params)
            if response:
                    print("Twitter API call successful")
                    dt=date.today()
                    iso_date=dt.isoformat()
                    response.update(
                        {"UserName": UserName, "Email": Email, "ISODate": iso_date, "SearchString": brand})
            else:
                print(
                    "Response does not have the news hence not sorting but sending fail email.")
                self.Email_Failed_Transaction(
                    "Response does not has the news hence not sorting but sending fail email.")
        except ClientError as e:
            print(e.response['Error']['Message'])
            self.Email_Failed_Transaction(
                "Exception error while getting news via API call.")
        else:
            print("News is retrieved as expected , hence returning now"),
            return response
            # print(response.json())

    def CreateUpdateEmailTemplate(self):
        try:
            print("get twitter data for the  run...")
            Getresponse = self.ses_client.get_template(TemplateName ='NewTwitterSentiment')
            if Getresponse['Template'] and Getresponse['ResponseMetadata']['HTTPStatusCode'] == 200:
                print("template alredy exists hence updating it now")
                self.ses_client.update_template(
                                Template ={
                                    "TemplateName": "NewTwitterSentiment",
                                    "SubjectPart": "Tweets on {{ SearchString }} for Date : {{ISODate}}",
                                    "HtmlPart": """<html>
                                                <head>
                                                <style>
                                                    table, td {
                                                    border: 1px solid black;
                                                    border-collapse: collapse;
                                                    }


                                                    th {
                                                    border: 1px solid black;
                                                    border-collapse: collapse;
                                                    font-weight: bold
                                                    }


                                                    td, th {
                                                    padding-left: 15px;
                                                    text-align: left;
                                                    }
                                                </style>
                                                </head>
                                                <body>
                                                <p style="font-family:'Futura Medium'">Hello {{ UserName }},</p>
                                                <p style="font-family:'Futura Medium'">Below are news on serach string {{ SearchString }} for Date : {{ISODate}}:</p>

                                                <table style="width:100%">
                                                    <col style="width:50%">
                                                    <col style="width:50%">
                                                    <tr bgcolor="yellow">
                                                        <td>AuthorId</td>
                                                        <td>CreateDate</td>
                                                        <td>RetweetCt</td>
                                                        <td>TweetType</td>
                                                        <td>Source</td>
                                                        <td>Text</td>
                                                    </tr>
                                                    {{#each tweet}}
                                                    <tr>
                                                    <td>{{author_id}}</td>
                                                    <td>{{created_at}}</td>
                                                    <td>{{public_metrics.retweet_count}}</td>
                                                    <td>{{referenced_tweets.type}}</td>
                                                    <td>{{source}}</td>
                                                    <td>{{text}}</td>
                                                    </tr>
                                                    {{/each}}
                                                </table>

                                                <p style="font-family:'Futura Medium'">Please check with jklacyn@amazon.com for any queries on the email.</p>

                                                <p style="font-family:'Futura Medium'">Best Regards,</p>
                                                <p style="font-family:'Futura Medium'">John Klacynski</p>
                                                </body>
                                                </html>
                                                """,
                                    "TextPart": """
                                                Hello {{ UserName }},

                                                Below are Tweets on brands {{ SearchString }} for Date : {{ISODate}}:

                                                    {{#each tweet}}
                                                    {{author_id}}
                                                    {{created_at}}
                                                    {{public_metrics.retweet_count}}
                                                    {{referenced_tweets.type}}
                                                    {{source}}
                                                    {{text}}
                                                    {{/each}}

                                                Please check with jklacyn@amazon.com for any queries on the email.

                                                Best Regards,
                                                John Klacynski
                                                """
                                }
                            )
            print("SES template is updated successfully")
            return True
        except ClientError as e:
            print("SES template is not there hence creating now")
            self.ses_client.create_template(
                                Template={
                                        "TemplateName": "NewTwitterSentiment",
                                        "SubjectPart": "News On {{ SearchString }} for Date : {{ISODate}}",
                                        "HtmlPart": """<html>
                                                        <head>
                                                        <style>
                                                            table, td {
                                                            border: 1px solid black;
                                                            border-collapse: collapse;
                                                            }
                                                            
                                                            
                                                            th {
                                                            border: 1px solid black;
                                                            border-collapse: collapse;
                                                            font-weight: bold
                                                            }
                                                            
                                                            
                                                            td, th {
                                                            padding-left: 15px;
                                                            text-align: left;
                                                            }
                                                        </style>
                                                        </head>
                                                        <body>
                                                        <p style="font-family:'Futura Medium'">Hello {{ UserName }},</p>
                                                        <p style="font-family:'Futura Medium'">Below are Tweets on your brand {{ SearchString }} for Date : {{ISODate}}:</p>
                                                        
                                                        <table style="width:100%">
                                                            <col style="width:50%">
                                                            <col style="width:50%">
                                                            <tr bgcolor="yellow">
                                                                <td>AuthorId</td>
                                                                <td>CreateDate</td>
                                                                <td>RetweetCt</td>
                                                                <td>TweetType</td>
                                                                <td>Source</td>
                                                                <td>Text</td>
                                                            </tr>
                                                            {{#each articles}}
                                                            <tr>
                                                            <td>{{author_id}}</td>
                                                            <td>{{created_at}}</td>
                                                            <td>{{public_metrics.retweet_count}}</td>
                                                            <td>{{referenced_tweets.type}}}</td>
                                                            <td>{{source}}</td>
                                                            <td>{{text}}</td>
                                                            </tr>
                                                            {{/each}}
                                                        </table>

                                                        <p style="font-family:'Futura Medium'">Please check with jklacyn@amazon.com for any queries on the email.</p>
                                                        
                                                        <p style="font-family:'Futura Medium'">Best Regards,</p>
                                                        <p style="font-family:'Futura Medium'">John Klacynski</p>
                                                        </body>
                                                        </html>
                                                        """,
                                            "TextPart": """
                                                        Hello {{ UserName }},
                                                        
                                                        Below are Tweets on your brand {{ SearchString }} for Date : {{ISODate}}:  
                                                                
                                                            {{#each articles}}
                                                            {{author_id}
                                                            {{created_at}}
                                                            {{public_metrics.retweet_count}}
                                                            {{referenced_tweets.type}}
                                                            {{source}}
                                                            {{text}}
                                                            {{/each}}

                                                        Please check with jklacyn@amazon.com for any queries on the email.
                                                        
                                                        Best Regards,
                                                        John Klacynski
                                                        """
                                        }
                                    )
            print("SES Template creation successful")
            return True

    def Email_Twitter(self , SourceEmail, ToEmail, finalresult):
        try:
            Sendresponse = self.ses_client.send_templated_email(
                                    Source=SourceEmail,
                                    Destination={
                                        'ToAddresses': [
                                            ToEmail
                                        ]
                                    },
                                    Template='NewTWitterSentiment',
                                    TemplateData= finalresult
                                )
        except Exception as e:
            print(str(e))
            self.Email_Failed_Transaction("Exception error while sending templated emails..!")
        if Sendresponse['ResponseMetadata']['HTTPStatusCode'] == 200:
            print('email sent successfully..')
        else :
            print('email sending failed..')

def main():
    print("Execution started.....")
    OjectNewsMails = NewsMails()
    CreateTemplate = OjectNewsMails.CreateUpdateEmailTemplate()
    if CreateTemplate:
        print("Email Template updated successfully...!!!!")
        TableResults = OjectNewsMails.GetAllDynamoDBRecord()
        if TableResults:
            print("dynamodb has the records in it.. hence processing now")
            for tableitem in TableResults:
                NewResults = OjectNewsMails.gettwitter(tableitem['brand'])
                if NewResults:
                    print("News results retrieved hence email now")
                    result = json.dumps(NewResults)
                    finalresultstr =  result.replace("null", "\"NoValue\"")
                    OjectNewsMails.Email_Twitter( "jklacyn@amazon.com", tableitem['email'], finalresultstr)
                    ReasonForFail = "News report email sent for user {} with email {} for search string {}".format(tableitem['user'], tableitem['email'], tableitem['brand'])
                    print(ReasonForFail)
                else:
                    print("No News results retrieved hence sending fail email now")
                    ReasonForFail = "No news results retrieved for user {} with email {} for search string {}".format(tableitem['user'], tableitem['email'], tableitem['brand'])
                    OjectNewsMails.Email_Failed_Transaction(ReasonForFail)
        else:
            print("Dynamodb does not has any email data, hence send fail email to John.")
            OjectNewsMails.Email_Failed_Transaction("Dynamodb does not has any email data")

main()