import boto3
import json

iam = boto3.client("iam")
region = "us-west-2"
account_id = boto3.client('sts').get_caller_identity()['Account']
bucket_name = f"bedrock-finetuning-{account_id}"

s3 = boto3.client("s3", region_name=region)

# For regions other than us-east-1, we must specify LocationConstraint
s3.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={"LocationConstraint": region}
)

print(f"S3 bucket created: {bucket_name} in {region}")


# Create IAM Role and Policy
role = iam.create_role(
    RoleName=f"Bedrock-Finetuning-Role-{account_id}",
    AssumeRolePolicyDocument=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "bedrock.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ] 
    })
)['Role']['RoleName']

policy_arn = iam.create_policy(
    PolicyName="Bedrock-Finetuning-Role-Policy",
    PolicyDocument=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    f"arn:aws:s3:::{bucket_name}",
                    f"arn:aws:s3:::{bucket_name}/*"
                ]
            }
        ]
    })
)['Policy']['Arn']

iam.attach_role_policy(
    RoleName=role,
    PolicyArn=policy_arn
)