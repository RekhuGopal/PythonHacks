import boto3

## How to stop an EC2 instance
def stop_instance(instance_id):
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    response = ec2_client.stop_instances(InstanceIds=[instance_id])
    print(response)

## Terminate an EC2 instance
def terminate_instance(instance_id):
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    response = ec2_client.terminate_instances(InstanceIds=[instance_id])
    print(response)


stop_instance("i-0016f12e547e92072")
terminate_instance("i-0016f12e547e92072")
