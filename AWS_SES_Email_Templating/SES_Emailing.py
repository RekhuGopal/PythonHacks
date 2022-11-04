from datetime import date, datetime, timezone, timedelta
from newsapi import NewsApiClient
import boto3
from botocore.exceptions import ClientError
import json


def getAllNews () :
        try :
            print("get news for the  run...")
            newsapi = NewsApiClient(api_key= "2b8bbd66c2e2403692a4e778e0697c21")
            from_date = datetime.now(timezone.utc) + timedelta(days=-3)
            end_time = datetime.now(timezone.utc) + timedelta(days=0)
            all_articles = newsapi.get_everything(q="Tenable Security",from_param=from_date,to=end_time,language="en",sort_by="relevancy")
            if all_articles :
                print("News APIs have returened..")
                # Dates
                dt = date.today()
                iso_date = dt.isoformat()
                all_articles.update({"UserName": "Rekhu Chinnarathod", "Email":"vrchinnarathod@gmail.com", "ISODate": iso_date, "SearchString": "Tenable Security"})
        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            print("News is retrieved as expected , hence retruning now"),
            return all_articles



# Get all news
ListOfNews = getAllNews ()

'''
#string to date conversion for sorting
for article in ListOfNews['articles'] :
    datetime_object = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
    article['publishedAt'] = datetime_object
'''

#Sort by date
ListOfNews['articles'].sort(key=lambda item:item['publishedAt'], reverse=True)

# convert dictionary into string
result = json.dumps(ListOfNews)
finalresult =  result.replace("null", "\"NoValue\"")

 # Create a new SES resource and specify a region.
client = boto3.client("ses",region_name="us-east-1")

response = client.get_template(TemplateName='NewAPIResultsMail')
print(response['ResponseMetadata']['HTTPStatusCode'])
'''
# Create SES templates
response = client.update_template(
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
'''
'''
####### Send templated emails.
Sendresponse = client.send_templated_email(
    Source='vrchinnarathod@gmail.com',
    Destination={
        'ToAddresses': [
            'vrchinnarathod@gmail.com',
        ]
    },
    Template='NewAPIResultsMail',
    TemplateData= finalresult
)

print(Sendresponse)
'''


