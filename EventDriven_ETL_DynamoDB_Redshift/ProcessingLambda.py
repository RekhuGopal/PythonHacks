import os
import psycopg2
import json
import boto3
from botocore.exceptions import ClientError

# Extract environment variables
dbname = os.environ['DB_NAME']
user = os.environ['DB_USER']
password = os.environ['DB_PASSWORD']
host = os.environ['DB_HOST']
port = os.environ['DB_PORT']


def lambda_handler(event, context):

    # Connect to Redshift
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = conn.cursor()
    except Exception as e:
        print(f"Error connecting to Redshift: {e}")
        return {
            'statusCode': 500,
            'body': f"Error connecting to Redshift: {e}"
        }

    # Process each record in the DynamoDB stream
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            # Extract the data from the DynamoDB stream record
            dynamodb_record = record['dynamodb']
            face_id = dynamodb_record['NewImage']['FaceId']['S']
            email = dynamodb_record['NewImage']['email']['S']
            name = dynamodb_record['NewImage']['name']['S']
            phone = dynamodb_record['NewImage']['phone']['S']
            title = dynamodb_record['NewImage']['title']['S']
            
            # Prepare the SQL query for insertion
            insert_query = """
            INSERT INTO cqpocsredshiftdemo (FaceId, email, name, phone, title)
            VALUES (%s, %s, %s, %s, %s)
            """
            data = (face_id, email, name, phone, title)
            
            try:
                # Execute the insert query
                cursor.execute(insert_query, data)
            except Exception as e:
                print(f"Error inserting data into Redshift: {e}")
                conn.rollback()
                continue  # Skip this record and move to the next one
    
    # Commit changes and close connections
    try:
        conn.commit()
    except Exception as e:
        print(f"Error committing transaction: {e}")
    finally:
        cursor.close()
        conn.close()

    return {
        'statusCode': 200,
        'body': 'Data transferred successfully'
    }
