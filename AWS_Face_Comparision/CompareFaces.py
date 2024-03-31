import boto3

rekognition = boto3.client('rekognition', region_name='us-west-2')
response = rekognition.compare_faces(
    SimilarityThreshold=90,
    SourceImage={
        'S3Object': {
            'Bucket': 'tonyfacecomparision',
            'Name': 'MugShotSide.png',
        },
    },
    TargetImage={
        'S3Object': {
            'Bucket': 'tonyfacecomparision',
            'Name': 'NewspaperA.png',
        },
    },
)
#print(response)
print(response['FaceMatches'])