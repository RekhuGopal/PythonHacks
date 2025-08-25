import boto3
import datetime

bedrock = boto3.client(service_name='bedrock', region_name='us-west-2')
account_id = boto3.client('sts').get_caller_identity()['Account']

# ✅ Use full ARN for base model in us-west-2
baseModelIdentifier = "arn:aws:bedrock:us-west-2::foundation-model/meta.llama3-2-3b-instruct-v1:0:128k"
customModelName = "meta-custom-model"

# Create job
datetime_string = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
response_ft = bedrock.create_model_customization_job(
    jobName=f"Finetune-Job-{datetime_string}",
    customizationType="FINE_TUNING",
    roleArn=f"arn:aws:iam::{account_id}:role/Bedrock-Finetuning-Role-{account_id}",
    hyperParameters={
        "epochCount": "5",
        "batchSize": "1",
        "learningRate": ".0001",
    },
    trainingDataConfig={"s3Uri": f"s3://bedrock-finetuning-{account_id}/train.jsonl"},
    outputDataConfig={"s3Uri": f"s3://bedrock-finetuning-{account_id}/finetuning-output"},
    customModelName=customModelName,
    baseModelIdentifier=baseModelIdentifier
)

jobArn = response_ft.get('jobArn')
print(jobArn)
