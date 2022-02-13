import boto3
client = boto3.client('comprehendmedical')
result = client.detect_entities(Text= 'cerealx 84 mg daily')
entities = result['Entities'];
for entity in entities:
    print('Entity', entity)