from datasets import load_dataset
import boto3
import json
import os

# Reference: https://github.com/aws/amazon-sagemaker-examples/blob/main/introduction_to_amazon_algorithms/jumpstart-foundation-models/llama-2-finetuning.ipynb 
dolly_dataset = load_dataset("databricks/databricks-dolly-15k", split="train")

# To train for question answering/information extraction, you can replace the assertion in next line to example["category"] == "closed_qa"/"information_extraction".
dataset = dolly_dataset.filter(lambda example: example["category"] == "classification")
dataset = dataset.remove_columns("category")

# We split the dataset into two where test data is used to evaluate at the end.
train_and_test_dataset = dataset.train_test_split(test_size=0.1)

# Dumping the training data to a local file to be used for training.
# dataset.to_json("fulldata.jsonl")
# train_and_test_dataset["train"].to_json("train.jsonl")
# train_and_test_dataset["test"].to_json("test.jsonl")

dataset_dir = "dataset"
def format_save_dataset(filename, dataset):
    os.makedirs(dataset_dir, exist_ok=True)
    with open(f"{dataset_dir}/{filename}", "w") as f:
        for i in dataset:
            instruction = i["instruction"]
            context = i["context"]
            response = i["response"]
            # template = {
            #     "prompt": "Below is an instruction that describes a task, paired with an input that provides further context. "
            #     "Write a response that appropriately completes the request.\n\n"
            #     f"### Instruction:\n{instruction}\n\n### Input:\n{context}\n\n",
            #     "completion": f"{response}",
            # }
            template = {
                "prompt": f"Write a response that appropriately completes the instruction. \n\nInstruction: {instruction}",
                "completion": f"{response}",
            }
            json.dump(template, f)
            f.write('\n')
    return 

# format_save_dataset("fulldataset.jsonl", dataset)
format_save_dataset("train.jsonl", train_and_test_dataset["train"])
format_save_dataset("test.jsonl", train_and_test_dataset["test"])

# Upload dataset to S3 bucket
s3 = boto3.client('s3')
account_id = boto3.client('sts').get_caller_identity()['Account']
bucket_name = f"bedrock-finetuning-{account_id}"

for root, dirs, files in os.walk(dataset_dir):
    for file in files:
        full_path = os.path.join(root, file)
        relative_path = os.path.relpath(full_path, dataset_dir)
        s3.upload_file(full_path, bucket_name, relative_path)