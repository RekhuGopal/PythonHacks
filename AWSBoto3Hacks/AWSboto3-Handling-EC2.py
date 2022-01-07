import boto3
import logging
from datetime import date, datetime
import json

# Helper method to serialize datetime fields
def json_datetime_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

## Create Key pair
def Create_EC2KeyPair(AWS_REGION):
    try:
        ec2_response = boto3.resource('ec2', region_name=AWS_REGION)
        result_keypair = ec2_response.create_key_pair(
                                    KeyName='cqpocs_key',
                                    DryRun=False,
                                    KeyType='rsa',
                                )
        if result_keypair:
            print("Key pair created successfull..!")
    except Exception as e:
        logging.error(e)
        return False
    return True

## Create EC2 Instances
def Create_EC2Instance (AWS_REGION, KEY_PAIR_NAME, AMI_ID ):
    try:
        ec2_response = boto3.resource('ec2', region_name=AWS_REGION)
        instances = ec2_response.create_instances(
            MinCount = 1,
            MaxCount = 1,
            ImageId=AMI_ID,
            InstanceType='t2.micro',
            KeyName=KEY_PAIR_NAME,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'cqpocs_demo'
                        },
                    ]
                },
            ]
        )

        for instance in instances:
            print(f'EC2 instance "{instance.id}" has been launched')
            instance.wait_until_running()
            print(f'EC2 instance "{instance.id}" has been started')
    except Exception as e:
        logging.error(e)
        return False
    return True

## List All EC2 Instances
def Getall_EC2Instance(AWS_REGION):
    try:
        ec2_response = boto3.resource('ec2', region_name=AWS_REGION)
        instances = ec2_response.instances.all()
        for instance in instances:
            print(f'EC2 instance {instance.id}" information:')
            print(f'Instance state: {instance.state["Name"]}')
            print(f'Instance AMI: {instance.image.id}')
            print(f'Instance platform: {instance.platform}')
            print(f'Instance type: "{instance.instance_type}')
            print(f'Piblic IPv4 address: {instance.public_ip_address}')
    except Exception as e:
        logging.error(e)
        return False
    return True

## Filter EC2 Instances
def Filter_EC2Instance(AWS_REGION):
    try:
        ec2_response = boto3.resource('ec2', region_name=AWS_REGION)
        tag_value = 'dev'
        instances = ec2_response.instances.filter(
            Filters=[
                {
                    'Name': 'tag:Environment',
                    'Values': [
                        tag_value
                    ]
                }
            ]
        )
        print(f'Instances with tag Name value "{tag_value}":')
        for instance in instances:
            print(f'  - Instance ID: {instance.id}')
    except Exception as e:
        logging.error(e)
        return False
    return True

## Describe EC2 Instance properties
def Describe_EC2Instance(AWS_REGION, INSTANCE_ID):
    try:
        ec2_response = boto3.client('ec2', region_name=AWS_REGION)
        response = ec2_response.describe_instances(
            InstanceIds=[
                INSTANCE_ID,
            ],
        )
        print(f'Instance {INSTANCE_ID} attributes:')
        for reservation in response['Reservations']:
            print(json.dumps(
                    reservation,
                    indent=4,
                    default=json_datetime_serializer
                )
            )
    except Exception as e:
        logging.error(e)
        return False
    return True

## Tag EC2 Instances
def Tag_EC2Instance(AWS_REGION,INSTANCE_ID):
    try:
        ec2_response = boto3.resource('ec2', region_name=AWS_REGION)
        TAGS = [
            {
                'Key': 'Environment',
                'Value': 'dev'
            }
        ]
        instances = ec2_response.instances.filter(
            InstanceIds=[
                INSTANCE_ID,
            ],
        )
        for instance in instances:
            instance.create_tags(Tags=TAGS)
            print(f'Tags successfully added to the instance {instance.id}')
    except Exception as e:
        logging.error(e)
        return False
    return True

## Stop EC2 Instances
def Stop_EC2Instance(AWS_REGION,INSTANCE_ID):
    try:
        ec2_response = boto3.resource('ec2', region_name=AWS_REGION)
        instance = ec2_response.Instance(INSTANCE_ID)
        instance.stop()
        print(f'Stopping EC2 instance: {instance.id}')
        instance.wait_until_stopped()
        print(f'EC2 instance "{instance.id}" has been stopped')
    except Exception as e:
        logging.error(e)
        return False
    return True

## Start EC2 Instances
def Start_EC2Instance(AWS_REGION,INSTANCE_ID):
    try:
        ec2_response = boto3.resource('ec2', region_name=AWS_REGION)
        instance = ec2_response.Instance(INSTANCE_ID)
        instance.start()
        print(f'Starting EC2 instance: {instance.id}')
        instance.wait_until_running()
        print(f'EC2 instance "{instance.id}" has been started')
    except Exception as e:
        logging.error(e)
        return False
    return True

## Restart EC2 Instances
def Restart_EC2Instance(AWS_REGION,INSTANCE_ID):
    try:
        ec2_response = boto3.resource('ec2', region_name=AWS_REGION)
        instance = ec2_response.Instance(INSTANCE_ID)
        instance.reboot()
        print(f'EC2 instance "{instance.id}" has been rebooted')
    except Exception as e:
        logging.error(e)
        return False
    return True

## Terminate EC2 Instances
def Terminate_EC2Instance(AWS_REGION,INSTANCE_ID):
    try:
        ec2_response = boto3.resource('ec2', region_name=AWS_REGION)
        instance = ec2_response.Instance(INSTANCE_ID)
        instance.terminate()
        print(f'Terminating EC2 instance: {instance.id}')
        instance.wait_until_terminated()
        print(f'EC2 instance "{instance.id}" has been terminated')
    except Exception as e:
        logging.error(e)
        return False
    return True

# Static variables
AWS_REGION = "eu-west-1"
KEY_PAIR_NAME = "cqpocs_key"
AMI_ID = "ami-04dd4500af104442f"
INSTANCE_ID = "i-009fabdf30ca6a7f2"
'''
## Create Key pair
Create_EC2KeyPair(AWS_REGION)

## Call Create EC2 Instances
Create_EC2Instance (AWS_REGION, KEY_PAIR_NAME, AMI_ID)


## List All EC2 Instances
Getall_EC2Instance(AWS_REGION)


## Filter EC2 Instances
Filter_EC2Instance(AWS_REGION)

## Describe EC2 Instance properties
Describe_EC2Instance(AWS_REGION, INSTANCE_ID)

## Tag EC2 Instances
Tag_EC2Instance(AWS_REGION,INSTANCE_ID)


## Stop EC2 Instances
Stop_EC2Instance(AWS_REGION,INSTANCE_ID)


## Start EC2 Instances
Start_EC2Instance(AWS_REGION,INSTANCE_ID)



## Restart EC2 Instances
Restart_EC2Instance(AWS_REGION,INSTANCE_ID)

## Terminate EC2 Instances
Terminate_EC2Instance(AWS_REGION,INSTANCE_ID)
'''