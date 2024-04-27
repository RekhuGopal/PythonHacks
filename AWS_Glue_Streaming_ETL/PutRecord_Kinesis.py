import csv
import json
import boto3
import time
import string
import random

def generate(stream_name, kinesis_client):
    with open("./data/lab2/sample.csv", encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            partitionaKey = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 20))
            jsonMsg = json.dumps(rows)
            kinesis_client.put_record(StreamName = stream_name,
                                      Data = jsonMsg,
                                      PartitionKey = partitionaKey)
            print(jsonMsg)
            time.sleep(0.2)

if __name__ == '__main__':
    generate('glueworkshop', boto3.client('kinesis'))
