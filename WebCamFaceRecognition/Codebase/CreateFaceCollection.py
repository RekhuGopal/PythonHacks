import boto3

rekognition = boto3.client('rekognition')

response = rekognition.create_collection(
    CollectionId='100Collections',
    Tags={
        'Apptype': 'face'
    }
)


print(response)