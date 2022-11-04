from datetime import date, datetime, timezone, timedelta
from newsapi import NewsApiClient
import boto3
from botocore.exceptions import ClientError
import json


class NewsMails:
    def __init__(self):
        client = boto3.resource('dynamodb', region_name="us-east-1")
        self.table = client.Table('AllEmails')
        self.NewsApikey = '2b8bbd66c2e2403692a4e778e0697c21'
        self.ses_client = boto3.client('ses',region_name="us-east-1")

    def GetAllDynamoDBRecord (self):
        try :
            response = self.table.scan()
            emaildata = response['Items']
            while 'LastEvaluatedKey' in response:
                response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                emaildata.extend(response['Items'])
        except ClientError as e:
            print(e.response['Error']['Message'])
            self.Email_Failed_Transaction("Exception error while getting all DynamoDB records..!")
        else:
            print("Dynamo DB records returned , hence retruning now"),
            return emaildata

    def GetAllNews (self , search, UserName, Email) :
        try :
            print("get news for the  run...")
            newsapi = NewsApiClient(api_key= self.NewsApikey)
            from_date = datetime.now(timezone.utc) + timedelta(days=-3)
            end_time = datetime.now(timezone.utc) + timedelta(days=0)
            all_articles = newsapi.get_everything(q=search,from_param=from_date,to=end_time,language='en',sort_by='relevancy')
            print(all_articles)
            if all_articles :
                print("News APIs have returened..")
                dt = date.today()
                iso_date = dt.isoformat()
                all_articles.update({"UserName": UserName, "Email":Email, "ISODate": iso_date, "SearchString": search})
            if all_articles['articles']:
                print("Response has the news in it hence sorting")
                all_articles['articles'].sort(key=lambda item:item['publishedAt'], reverse=True)
            else:
                print("Response does not has the news hence not sorting but sending fail email.")
                self.Email_Failed_Transaction("Response does not has the news hence not sorting but sending fail email.")
        except ClientError as e:
            print(e.response['Error']['Message'])
            self.Email_Failed_Transaction("Exception error while getting news via API call.")
        else:
            print("News is retrieved as expected , hence retruning now"),
            return all_articles

    def CreateUpdateEmailTemplate(self):
        try :
            print("get news for the  run...")
            Getresponse = self.ses_client.get_template( TemplateName='NewAPIResultsMail')
            if Getresponse['Template'] and Getresponse['ResponseMetadata']['HTTPStatusCode'] == 200 :
                print("template alredy exists hence updating it now")
                self.ses_client.update_template( 
                                Template={
                                        "TemplateName": "NewAPIResultsMail",
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
                                                    <p style="font-family:'Futura Medium'">Below are news on serach string {{ SearchString }} for Date : {{ISODate}}:</p>
                                                    
                                                    <table style="width:100%">
                                                        <col style="width:50%">
                                                        <col style="width:50%">
                                                        <tr bgcolor="yellow">
                                                            <td>SourceId</td>
                                                            <td>SourceName</td>
                                                            <td>Author</td>
                                                            <td>Title</td>
                                                            <td>Description</td>
                                                            <td>Url</td>
                                                            <td>UrlToImage</td>
                                                            <td>PublishedAt</td>
                                                            <td>Content</td>
                                                        </tr>
                                                        {{#each articles}}
                                                        <tr>
                                                        <td>{{source.id}}</td>
                                                        <td>{{source.name}}</td>
                                                        <td>{{author}}</td>
                                                        <td>{{title}}</td>
                                                        <td>{{description}}</td>
                                                        <td>{{url}}</td>
                                                        <td>{{urlToImage}}</td>
                                                        <td>{{publishedAt}}</td>
                                                        <td>{{content}}</td>
                                                        </tr>
                                                        {{/each}}
                                                    </table>

                                                    <p style="font-family:'Futura Medium'">Please check with jaklacynski@protonmail.com for any queries on the email.</p>
                                                    
                                                    <p style="font-family:'Futura Medium'">Best Regards,</p>
                                                    <p style="font-family:'Futura Medium'">John Klacynski</p>
                                                    </body>
                                                    </html>
                                                    """,
                                        "TextPart": """
                                                    Hello {{ UserName }},
                                                    
                                                    Below are news on serach string {{ SearchString }} for Date : {{ISODate}}:  
                                                            
                                                        {{#each articles}}
                                                        {{source.id}}
                                                        {{source.name}}
                                                        {{author}}
                                                        {{title}}
                                                        {{description}}
                                                        {{url}}
                                                        {{urlToImage}}
                                                        {{publishedAt}}
                                                        {{content}}
                                                        {{/each}}

                                                    Please check with jaklacynski@protonmail.com for any queries on the email.
                                                    
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
                                        "TemplateName": "NewAPIResultsMail",
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
                                                    <p style="font-family:'Futura Medium'">Below are news on serach string {{ SearchString }} for Date : {{ISODate}}:</p>
                                                    
                                                    <table style="width:100%">
                                                        <col style="width:50%">
                                                        <col style="width:50%">
                                                        <tr bgcolor="yellow">
                                                            <td>SourceId</td>
                                                            <td>SourceName</td>
                                                            <td>Author</td>
                                                            <td>Title</td>
                                                            <td>Description</td>
                                                            <td>Url</td>
                                                            <td>UrlToImage</td>
                                                            <td>PublishedAt</td>
                                                            <td>Content</td>
                                                        </tr>
                                                        {{#each articles}}
                                                        <tr>
                                                        <td>{{source.id}}</td>
                                                        <td>{{source.name}}</td>
                                                        <td>{{author}}</td>
                                                        <td>{{title}}</td>
                                                        <td>{{description}}</td>
                                                        <td>{{url}}</td>
                                                        <td>{{urlToImage}}</td>
                                                        <td>{{publishedAt}}</td>
                                                        <td>{{content}}</td>
                                                        </tr>
                                                        {{/each}}
                                                    </table>

                                                    <p style="font-family:'Futura Medium'">Please check with jaklacynski@protonmail.com for any queries on the email.</p>
                                                    
                                                    <p style="font-family:'Futura Medium'">Best Regards,</p>
                                                    <p style="font-family:'Futura Medium'">John Klacynski</p>
                                                    </body>
                                                    </html>
                                                    """,
                                        "TextPart": """
                                                    Hello {{ UserName }},
                                                    
                                                    Below are news on serach string {{ SearchString }} for Date : {{ISODate}}:  
                                                            
                                                        {{#each articles}}
                                                        {{source.id}}
                                                        {{source.name}}
                                                        {{author}}
                                                        {{title}}
                                                        {{description}}
                                                        {{url}}
                                                        {{urlToImage}}
                                                        {{publishedAt}}
                                                        {{content}}
                                                        {{/each}}

                                                    Please check with jaklacynski@protonmail.com for any queries on the email.
                                                    
                                                    Best Regards,
                                                    John Klacynski
                                                    """
                                    }
                                )
            print("SES Templete creation successful")
            return True

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
            self.Email_Failed_Transaction("Exception error while sending templated emails..!")
        if Sendresponse['ResponseMetadata']['HTTPStatusCode'] == 200:
            print('email sent successfully..')
        else :
            print('email sending failed..')

    def Email_Failed_Transaction(self, ReasonForFailure):
        try:
            print("Sending failed email now....")
            body_text = """
                Hello John,
                
                Sending news report automation has encountered an error..!!          
                Please check CloudWatch logs of lambda to get more insights.

                Reason for failure is : """ + ReasonForFailure + """
                
                Best Regards,
                Cloud Quick Labs.
                """

            # The HTML body of the email.
            body_html = """<html>
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
                <p style="font-family:'Futura Medium'">Hello John,</p>

                <p style="font-family:'Futura Medium'">Sending news report automation has encountered an error..!!</p>
                <p style="font-family:'Futura Medium'">Please check CloudWatch logs of lambda to get more insights.</p>

                <p style="font-family:'Futura Medium'">Reason for failure is : """ + ReasonForFailure + """</p>
                
                <p style="font-family:'Futura Medium'">Best Regards,</p>
                <p style="font-family:'Futura Medium'">Cloud Quick Labs.</p>
                </body>
                </html>
                """
            # Provide the contents of the email.
            send_mail_response = self.ses_client.send_email(
                Source="Cloud-Quick-Labs@automations.com",
                Destination={
                    'ToAddresses': ["vrchinnarathod@gmail.com"]
                },
                Message={
                    'Subject': {
                        'Data': "Schdeduled News Report Email Delivery Failed."

                    },
                    'Body': {
                        'Text': {
                            'Data': body_text

                        },
                        'Html': {
                            'Data': body_html

                        }
                    }
                }
            )
            print(send_mail_response)
            return send_mail_response
        except Exception as e:
            print(str(e))
            return str(e)

def lambda_handler(event, context):
    print("Execution started.....")
    OjectNewsMails = NewsMails() 
    CreateTemplate = OjectNewsMails.CreateUpdateEmailTemplate()
    if CreateTemplate :
        print("Email Template updated successfully...!!!!")
        TableResults = OjectNewsMails.GetAllDynamoDBRecord()
        if TableResults:
            print("dynamodb has the records in it.. hence processing now")
            for tableitem in TableResults:
                NewResults = OjectNewsMails.GetAllNews(tableitem['google-search'], tableitem['user'], tableitem['email'] )
                if NewResults :
                    print("News results retrieved hence email now")
                    result = json.dumps(NewResults)
                    finalresultstr =  result.replace("null", "\"NoValue\"")
                    OjectNewsMails.Email_News( "vrchinnarathod@gmail.com", tableitem['email'], finalresultstr)
                    ReasonForFail = "News report email sent for user {} with email {} for search string {}".format(tableitem['user'], tableitem['email'], tableitem['google-search'])
                    print(ReasonForFail)
                else:
                    print("No News results retrieved hence sending fail email now")
                    ReasonForFail = "No news results retrieved for user {} with email {} for search string {}".format(tableitem['user'], tableitem['email'], tableitem['google-search'])
                    OjectNewsMails.Email_Failed_Transaction(ReasonForFail)
        else:
            print("Dynamodb does not has any email data, hence send fail email to John.")
            OjectNewsMails.Email_Failed_Transaction("Dynamodb does not has any email data")
    else :
        print("Email Template updated Failed...!!!!")
