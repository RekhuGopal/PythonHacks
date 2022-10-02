import json
import psycopg2
import os
import boto3
import csv

## This is the tool
def lambda_handler(event, context):
    print("event collected is {}".format(event))
    for record in event['Records'] :
        s3_bucket = record['s3']['bucket']['name']
        print("Bucket name is {}".format(s3_bucket))
        s3_key = record['s3']['object']['key']
        print("Bucket key name is {}".format(s3_key))
        from_path = "/tmp/{}".format(s3_key)
        print("from path {}".format(from_path))

        #initiate s3 client 
        s3 = boto3.client('s3')

        #Download object to the file    
        s3.download_file(s3_bucket, s3_key, from_path)
        print("donwloaded successfully....")
        
        dbname = os.getenv('dbname')
        host = os.getenv('host')
        user = os.getenv('user')
        password = os.getenv('password')
        tablename = os.getenv('tablename')
        connection = psycopg2.connect(dbname = dbname,
                                       host = host,
                                       port = '5432',
                                       user = user,
                                       password = password)
                                       
        print('after connection....')
        curs = connection.cursor()
        print('after cursor....')
        # opening the CSV file
        with open(from_path, mode ='r')as file:
   
            # reading the CSV file
            csvFile = csv.reader(file)
 
            # displaying the contents of the CSV file
            for lines in csvFile:
                print(type(lines))
                print(lines[0])
                print(lines[1])
                print(lines[2])
                querry = "INSERT INTO cqpocsredshiftdemo (industry_name_ANZSIC,rme_size_grp,variables) VALUES ('{}', '{}', '{}');".format(lines[0], lines[1], lines[2])
                print("query is {}".format(querry))
                print('after querry....')
                curs.execute(querry)
        connection.commit()
        #print(curs.fetchmany(3))
        print('after execute....')
        curs.close()
        print('after curs close....')
        connection.close()
        print('after connection close....')
        print('wow..executed....')
        os.remove(from_path)
        print('file removed from lambda storage....')