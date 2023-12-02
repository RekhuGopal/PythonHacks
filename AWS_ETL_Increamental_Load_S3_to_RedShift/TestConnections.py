import os
import psycopg2

dbnameValue = "dev"
hostValue = "workspacenames.357171621133.us-west-2.redshift-serverless.amazonaws.com"
userName = "admin"
passwordValue = "Test#123456"
connection = psycopg2.connect(dbname = dbnameValue,
                            host = hostValue,
                            port = '5439',
                            user = userName,
                            password = passwordValue)        
print('after connection....')
curs = connection.cursor()
print('after cursor....')
querry = "INSERT INTO dev.public.Persons (industry_name_ANZSIC, rme_size_grp, variables) VALUES (3, 'value2', 'value3')"
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