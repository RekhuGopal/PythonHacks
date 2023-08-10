#write code to list all s3 bukcet prsent in account

import boto3


def list_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        print(bucket['Name'])

list_buckets()

# write code to create ec2 spot instance


import boto3

def create_spot_instance():
    ec2 = boto3.client('ec2')
    response = ec2.request_spot_instances(
        InstanceCount=1,
        LaunchSpecification={
            'ImageId': 'ami-0d5eff06f840b45e9',
            'KeyName': 'ec2-keypair',
            'InstanceType': 't2.micro'
        },
        SpotPrice='0.01',
        Type='one-time'
    )
    print(response)




