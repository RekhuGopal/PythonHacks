"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3

# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('my-bucket-pulumi-cloudquicklabs',
website=s3.BucketWebsiteArgs(
        index_document="index.html",
    )
)

bucketObject = s3.BucketObject(
    'index.html',
    acl='public-read',
    content_type='text/html',
    bucket=bucket.id,
    source=pulumi.FileAsset('index.html')
)
'''
bucket = s3.Bucket('my-bucket-pulumi-cloudquicklabs',
    website=s3.BucketWebsiteArgs(
        index_document="index.html",
    ))
    
bucketObject = s3.BucketObject(
    'index.html',
    acl='public-read',
    content_type='text/html',
    bucket=bucket.id,
    source=pulumi.FileAsset('index.html'),
)   
'''
# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)

pulumi.export('bucket_endpoint', pulumi.Output.concat('http://', bucket.website_endpoint))
