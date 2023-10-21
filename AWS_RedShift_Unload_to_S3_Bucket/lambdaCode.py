import os
import psycopg2

def lambda_handler(event, context):
    dbnameValue = os.getenv('dbname')
    hostValue = os.getenv('host')
    userName = os.getenv('user')
    passwordValue = os.getenv('password')
    connection = psycopg2.connect(dbname = dbnameValue,
                                host = hostValue,
                                port = '5439',
                                user = userName,
                                password = passwordValue)        
    print('after connection....')
    curs = connection.cursor()
    print('after cursor....')
    querry = "unload ('select * from dev.public.test') to 's3://redshift-table-to-s3-bucket/unload/test_' iam_role 'arn:aws:iam::357171621133:role/ETLlambdaAccessRole' ALLOWOVERWRITE JSON;"
    print("query is {}".format(querry))
    print('after querry....')
    curs.execute(querry)
    connection.commit()
    print('after execute....')
    curs.close()
    print('after curs close....')
    connection.close()
    print('after connection close....')
    print('wow..executed....')