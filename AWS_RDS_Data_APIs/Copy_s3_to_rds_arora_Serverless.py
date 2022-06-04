import boto3

def lambda_handler(event, context):
    ## Endpoint not enabled , use below command to enable it 
    #aws rds modify-db-cluster --db-cluster-identifier cloudquicklabs --enable-http-endpoint --apply-immediately
    rds_client = boto3.client('rds-data')
    database_name = "Labs"
    db_cluster_arn = "arn:aws:rds:ap-south-1:357171621133:cluster:cloudquicklabs"
    db_credentials_secrets_store_arn = "arn:aws:secretsmanager:ap-south-1:357171621133:secret:Creds-B9OnMD"

    def execute_statement(sql, sql_parameters=[]):
        response = rds_client.execute_statement(
            secretArn=db_credentials_secrets_store_arn,
            database=database_name,
            resourceArn=db_cluster_arn,
            sql=sql,
            parameters=sql_parameters
        )
        return response

    def batch_execute_statement(sql, sql_parameter_sets):
        response = rds_client.batch_execute_statement(
            secretArn=db_credentials_secrets_store_arn,
            database=database_name,
            resourceArn=db_cluster_arn,
            sql=sql,
            parameterSets=sql_parameter_sets
        )
        return response
    '''
    ## Parameterised Insert
    sql = 'insert into package (package_name, package_version) values (:package_name, :package_version)'
    sql_parameters = [
        {'name':'package_name', 'value':{'stringValue': 'package-2'}},
        {'name':'package_version', 'value':{'stringValue': 'version-1'}}
    ]
    response = execute_statement(sql, sql_parameters)
    print(f'Number of records updated: {response["numberOfRecordsUpdated"]}')
    '''


    ## Simple Get all querry
    response = execute_statement('select * from package')
    print(response['records'])
    '''
    ## Parameterised Get
    sql = 'select * from package where package_name=:package_name'
    package_name = 'package2'
    sql_parameters = [{'name':'package_name', 'value':{'stringValue': f'{package_name}'}}]
    response = execute_statement(sql, sql_parameters)
    print(response['records'])


    ## Batch Insert
    sql = 'insert into package (package_name, package_version) values (:package_name, :package_version)'
    sql_parameter_sets = []
    for i in range(1,11):
        entry = [
                    {'name':'package_name', 'value':{'stringValue': f'package{i}'}},
                    {'name':'package_version', 'value':{'stringValue': f'version{i}'}}
            ]
        sql_parameter_sets.append(entry)
    response = batch_execute_statement(sql, sql_parameter_sets)
    print(f'Number of records updated: {len(response["updateResults"])}')


    ## Committing or roll back.
    transaction = rds_client.begin_transaction(
        secretArn=db_credentials_secrets_store_arn,
        resourceArn=db_cluster_arn,
        database=database_name)
    try:
        sql = 'insert into package (package_name, package_version) values (:package_name, :package_version)'
        sql_parameter_sets = []
        for i in range(30,40):
            entry = [
                    {'name':'package_name', 'value':{'stringValue': f'package{i}'}},
                    {'name':'package_version', 'value':{'stringValue': f'version{i}'}}
            ]
            sql_parameter_sets.append(entry)
        response = batch_execute_statement(sql, sql_parameter_sets, transaction['transactionId'])
    except Exception:
        transaction_response = rds_client.rollback_transaction(
            secretArn=db_credentials_secrets_store_arn,
            resourceArn=db_cluster_arn,
            transactionId=transaction['transactionId'])
    else:
        transaction_response = rds_client.commit_transaction(
            secretArn=db_credentials_secrets_store_arn,
            resourceArn=db_cluster_arn,
            transactionId=transaction['transactionId'])
        print(f'Number of records updated: {len(response["updateResults"])}')
    print(f'Transaction Status: {transaction_response["transactionStatus"]}')
    '''