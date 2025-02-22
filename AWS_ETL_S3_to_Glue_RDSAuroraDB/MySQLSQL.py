import logging
import os
import boto3
import csv
import pymysql
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
    port = int(os.getenv('DB_PORT'))  # Default MySQL port is 3306

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
        return {'statusCode': 500, 'body': f"Error downloading file from S3: {e}"}

    # Parse CSV file content
    try:
        csv_file = StringIO(csv_content)
        csv_reader = csv.DictReader(csv_file)
        rows = [row for row in csv_reader]
        logger.info(f"CSV file parsed successfully. {len(rows)} records found.")
    except Exception as e:
        logger.error(f"Error parsing CSV file: {e}")
        return {'statusCode': 500, 'body': f"Error parsing CSV file: {e}"}

    # Establish the connection to the MySQL database
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=dbname,
            port=port,
            cursorclass=pymysql.cursors.DictCursor
        )
        logger.info("Connection to database successful!")
    except pymysql.MySQLError as e:
        logger.error(f"Error connecting to database: {e}")
        return {'statusCode': 500, 'body': f"Error connecting to database: {e}"}

    # Create a cursor object to interact with the database
    try:
        with conn.cursor() as cursor:
            # Step 1: Create table if it doesn't exist
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS demo.employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                email VARCHAR(100),
                hire_date DATE,
                salary DECIMAL(10,2)
            );
            '''
            cursor.execute(create_table_query)
            conn.commit()
            logger.info("Table created successfully!")

            # Step 2: Insert records from CSV into the table
            insert_record_query = '''
            INSERT INTO demo.employees (first_name, last_name, email, hire_date, salary) 
            VALUES (%s, %s, %s, %s, %s);
            '''
            for row in rows:
                cursor.execute(insert_record_query, (row['first_name'], row['last_name'], row['email'], row['hire_date'], row['salary']))
            conn.commit()
            logger.info(f"{len(rows)} records inserted successfully!")

            # Step 3: Fetch and print all data from the table
            select_query = 'SELECT * FROM demo.employees;'
            cursor.execute(select_query)
            all_records = cursor.fetchall()
            logger.info("Data from demo.employees table:")
            for record in all_records:
                logger.info(f"Row: {record}")
    
    except Exception as e:
        logger.error(f"Error during database operations: {e}")
        conn.rollback()
        return {'statusCode': 500, 'body': f"Error during database operations: {e}"}
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed.")

    return {'statusCode': 200, 'body': 'Database operations completed successfully'}
