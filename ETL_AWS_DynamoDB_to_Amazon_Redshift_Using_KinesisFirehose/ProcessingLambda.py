import json
import boto3

firehose = boto3.client('firehose')
deliveryStreamName = 'PUT-RED-8o70r'
def convertToFirehoseRecord(ddbRecord):
    newImage = ddbRecord['NewImage']
    firehoseRecord = "{},{},{},{},{},{}".format(newImage['ID']['S'],
    newImage['Name']['S'],
    newImage['City']['S'],
	newImage['Email']['S'],
	newImage['Designation']['S'],
    newImage['PhoneNumber']['S']) + '\n'
    return firehoseRecord
def lambda_handler(event, context):
    print(event)
    for record in event['Records']:
        print(record)
        ddbRecord = record['dynamodb']
        print('DDB Record: ' + json.dumps(ddbRecord))
        
        firehoseRecord = convertToFirehoseRecord(ddbRecord)
        print('Firehose Record: ' + firehoseRecord)
        
        result = firehose.put_record(DeliveryStreamName=deliveryStreamName, Record={ 'Data': firehoseRecord})
        print(result)
    return 'processed {} records.'.format(len(event['Records']))
