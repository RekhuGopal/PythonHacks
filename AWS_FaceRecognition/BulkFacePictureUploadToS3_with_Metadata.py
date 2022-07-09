import boto3

s3 = boto3.resource('s3')

# Get list of objects for indexing
images=[('1.jpg','APJ Kalam'),
      ('2.jpg','CV Raman'),
      ('3.jpg','David Bekhm'),
      ('4.png','Albert Einstein'),
      ('5.jpg','Isaac Newton'),
      ('6.png','Lionel Messi'),
      ('7.jpeg','Nikola Tesla'),
      ('8.jpg','Cristiano Ronaldo'),
      ('9.jpg','Sunil Chhetri')
      ]

# Iterate through list to upload objects to S3   
for image in images:
    file = open(image[0],'rb')
    object = s3.Object('facecollectionbucket','index/'+ image[0])
    ret = object.put(Body=file,
                    Metadata={'FullName':image[1]}
                    )