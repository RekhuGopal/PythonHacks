import boto3

client = boto3.client('rds-data')

response = client.execute_statement(
    secretArn   = 'arn:aws:secretsmanager:us-east-1:123456789012:secret:aurora-serverless-data-api-sl-admin-2Ir1oL',
    database    = 'users',
    resourceArn = 'arn:aws:rds:us-east-1:123456789012:cluster:aurora-sl-1',
    sql         = 'select * from users'
)

for user in response['records']:
  userid     = user[0]['stringValue']
  first_name = user[1]['stringValue']
  last_name  = user[2]['stringValue']
  print(userid + ' ' + first_name + ' ' + last_name)