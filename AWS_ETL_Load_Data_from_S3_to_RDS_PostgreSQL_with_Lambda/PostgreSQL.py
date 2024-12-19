import psycopg2
import logging
import os
import boto3
import csv
from io import StringIO

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize the S3 client
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Retrieve database connection parameters from environment variables
    host = os.getenv('DB_HOST')
    dbname = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    port = int(os.getenv('DB_PORT'))  # Default PostgreSQL port

    # Get the S3 bucket name and file name from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    # Download the CSV file from S3
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        csv_content = response['Body'].read().decode('utf-8')
        logger.info(f"CSV file {file_key} successfully fetched from S3.")
    except Exception as e:
        logger.error(f"Error downloading file from S3: {e}")
        return {
            'statusCode': 500,
            'body': f"Error downloading file from S3: {e}"
        }

    # Parse CSV file content
    try:
        csv_file = StringIO(csv_content)
        csv_reader = csv.DictReader(csv_file)  # Read the file as a dictionary (header -> fieldname)
        rows = [row for row in csv_reader]  # Collect all rows
        logger.info(f"CSV file parsed successfully. {len(rows)} records found.")
    except Exception as e:
        logger.error(f"Error parsing CSV file: {e}")
        return {
            'statusCode': 500,
            'body': f"Error parsing CSV file: {e}"
        }

    # Establish the connection to the PostgreSQL database
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        logger.info("Connection to database successful!")
    except psycopg2.OperationalError as e:
        logger.error(f"Error connecting to database: {e}")
        return {
            'statusCode': 500,
            'body': f"Error connecting to database: {e}"
        }

    # Create a cursor object to interact with the database
    try:
        with conn.cursor() as cursor:
            # Step 1: Create table if it doesn't exist (same as before)
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS employee (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                age INTEGER
            );
            '''
            cursor.execute(create_table_query)
            conn.commit()  # Commit changes
            logger.info("Table created successfully!")

            # Step 2: Insert records from CSV into the table
            insert_record_query = '''
            INSERT INTO employee (name, age) 
            VALUES (%s, %s);
            '''
            for row in rows:
                cursor.execute(insert_record_query, (row['name'], row['age']))  # Insert data
            conn.commit()  # Commit changes
            logger.info(f"{len(rows)} records inserted successfully!")

            # Step 3: Fetch and print all data from the table
            select_query = 'SELECT * FROM employee;'
            cursor.execute(select_query)
            all_records = cursor.fetchall()  # Fetch all rows from the result
            logger.info("Data from employee table:")
            for record in all_records:
                logger.info(f"Row: {record}")

    except Exception as e:
        logger.error(f"Error during database operations: {e}")
        conn.rollback()  # Rollback if error occurs
        return {
            'statusCode': 500,
            'body': f"Error during database operations: {e}"
        }
    finally:
        # Close the connection
        if conn:
            conn.close()
            logger.info("Database connection closed.")

    return {
        'statusCode': 200,
        'body': 'Database operations completed successfully'
    }
