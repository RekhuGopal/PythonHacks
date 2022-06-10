import boto3
from botocore.exceptions import ClientError

def send_email(accountId, bucketName):
    SENDER = "xyz@gmail.com" # must be verified in AWS SES Email
    RECIPIENT = "xyz@gmail.com" # must be verified in AWS SES Email

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = 'Resource Creation Notification..!! S3 bucket name :'+bucketName+' and Account ID is : '+accountId
    

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Hi There...\r\n"
                "AWS resource creation indentified please validate..\n"
                "Thanks and Regards\n"
                "AWS-EVENT-DRIVEN-AUTOMATION"
                )
                
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Hi There...</h1>
	
    <p>AWS resource creation indentified please validate.. </p>
	
    <p>Thanks and Regards</p>
    <p>AWS Event-driven Solution</p>
    
    </body>
    </html>
                """            

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
        
                        'Data': BODY_HTML
                    },
                    'Text': {
        
                        'Data': BODY_TEXT
                    },
                },
                'Subject': {

                    'Data': SUBJECT
                },
            },
            Source=SENDER
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

def lambda_handler(event, context):
    # TODO implement
    print(event)
    send_email(event['detail']['userIdentity']['accountId'],event['detail']['requestParameters']['bucketName'])