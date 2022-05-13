import json
import psycopg2
import os

def ExecuteQuerries():
    conn = psycopg2.connect(dbname = "vehicle",
                                    host = "cloudquicklabs-instance-1.clg2kzrollbh.ap-south-1.rds.amazonaws.com",
                                    port = '5432',
                                    user = "postgres",
                                    password = "PsSW0rd123")
                                    
    #Setting auto commit false
    conn.autocommit = True

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Insert data
    cursor.execute('''INSERT INTO cqpocsredshiftdemo (industry_name_ANZSIC,rme_size_grp,variables) VALUES ('RRR2', 'Paul2', 'xyz2')''')

    #Update data
    cursor.execute("UPDATE cqpocsredshiftdemo SET industry_name_ANZSIC ='Hello', rme_size_grp ='lab2' WHERE variables like 'xyz2'")

    #Delete data
    cursor.execute("DELETE FROM cqpocsredshiftdemo WHERE variables like 'xyz2'")

    #Retrieving data
    cursor.execute('Select * from cqpocsredshiftdemo')

    #Fetching 1st row from the table
    #result = cursor.fetchone();
    #print(result)

    #Fetching 1st row from the table
    result = cursor.fetchall();
    print(result)

    #Commit your changes in the database
    conn.commit()

    #Closing the connection
    conn.close()

ExecuteQuerries()