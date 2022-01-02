import boto3
import json
import datetime

client = boto3.client('cloudtrail')
response = client.lookup_events(
    LookupAttributes=[
        {
            'AttributeKey': 'EventId'|'EventName'|'ReadOnly'|'Username'|'ResourceType'|'ResourceName'|'EventSource'|'AccessKeyId',
            'AttributeValue': 'string'
        },
    ],
    StartTime=datetime(2015, 1, 1),
    EndTime=datetime(2015, 1, 1),
    EventCategory='insight',
    MaxResults=123,
    NextToken='string'
)

print(response)