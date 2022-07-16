import boto3
import io
from PIL import Image

rekognition = boto3.client('rekognition', region_name='ap-south-1')
dynamodb = boto3.client('dynamodb', region_name='ap-south-1')
    
image = Image.open("LM.jpg")
stream = io.BytesIO()
image.save(stream,format="JPEG")
image_binary = stream.getvalue()


response = rekognition.search_faces_by_image(
        CollectionId='family_collection',
        Image={'Bytes':image_binary}                                       
        )
    
for match in response['FaceMatches']:
    print (match['Face']['FaceId'],match['Face']['Confidence'])
        
    face = dynamodb.get_item(
        TableName='family_collection',  
        Key={'RekognitionId': {'S': match['Face']['FaceId']}}
        )
    
    if 'Item' in face:
        print ("The face identified is:", face['Item']['FullName']['S'])
    else:
        print ('no match found in person lookup')