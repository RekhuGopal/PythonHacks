from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="<Open API Key>",
    api_version="2024-05-01-preview",   # Use latest preview version
    azure_endpoint="<Endpoint>"
)

jobs = client.fine_tuning.jobs.list()

for job in jobs.data:
    print(f"ID: {job.id}")
    print(f"Status: {job.status}")
    print(f"Base Model: {job.model}")  # use 'model', not 'base_model'
    print(f"Fine-tuned Model: {job.fine_tuned_model}")
    print(f"Created at: {job.created_at}")
    print("--------------")

    # If you want to see all available fields:
    print(job.model_dump())