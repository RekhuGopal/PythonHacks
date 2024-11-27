import json
import boto3
import string
import random
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    try:
        # Create an S3 client
        s3 = boto3.client("s3")

        # Extract the JSON object from the event body
        get_content = event["body-json"]  # This is expected to be a dictionary

        # Generate a random filename for the JSON file
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        # Convert the dictionary to a JSON string (this will be the content uploaded to S3)
        json_data = json.dumps(get_content)

        # Upload the JSON content to the S3 bucket
        s3_upload = s3.put_object(Bucket="databucketsourceside", Key=filename + ".json", Body=json_data)

        # Return success message
        return {
            'statusCode': 200,
            'body': json.dumps('The Object is Uploaded successfully!')
        }
    
    except KeyError as e:
        # Handle missing keys in the event (e.g., "body-json")
        return {
            'statusCode': 400,
            'body': json.dumps(f"KeyError: Missing key in the event data: {str(e)}")
        }
    
    except ClientError as e:
        # Handle S3 upload failures or AWS-related issues
        return {
            'statusCode': 500,
            'body': json.dumps(f"S3 Upload Error: {str(e)}")
        }
    
    except Exception as e:
        # Handle any other unexpected exceptions
        return {
            'statusCode': 500,
            'body': json.dumps(f"An unexpected error occurred: {str(e)}")
        }
