import boto3
from trp import Document

#Text detection from documents:
# Document
s3BucketName = "demotextractcqpocs"
documentName = "Test2.JPG"

# Amazon Textract client
textractmodule = boto3.client('textract')

# Call Amazon Textract
response = textractmodule.detect_document_text(
    Document={
        'S3Object': {
            'Bucket': s3BucketName,
            'Name': documentName
        }
    })

#print(response)

# Print detected text
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        print ('\033[92m'+item["Text"]+'\033[92m')


# Call Amazon Textract
response = textractmodule.analyze_document(
    Document={
        'S3Object': {
            'Bucket': s3BucketName,
            'Name': documentName
        }
    },
    FeatureTypes=["FORMS"])

#print(response)

doc = Document(response)

for page in doc.pages:
    # Print fields
    print("Fields:")
    for field in page.form.fields:
        print("Key: {}, Value: {}".format(field.key, field.value))