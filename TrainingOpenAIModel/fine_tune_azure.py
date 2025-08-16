import os
from openai import OpenAI
import json
import time

# --- Environment ---
AZURE_OPENAI_API_KEY = "<OPEN API KEY>"
AZURE_OPENAI_ENDPOINT = "<OPEN API ENDPOINT>"
AZURE_OPENAI_API_VERSION = "2024-10-21"

client = OpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    base_url=f"{AZURE_OPENAI_ENDPOINT}/openai",
    default_query={"api-version": AZURE_OPENAI_API_VERSION},
)

# --- Upload training data ---
with open("train.jsonl", "rb") as f:
    train_file = client.files.create(file=f, purpose="fine-tune")
print("Training file uploaded:", train_file.id)

# Optional validation file
valid_file = None
if os.path.exists("validation.jsonl"):
    with open("validation.jsonl", "rb") as f:
        valid_file = client.files.create(file=f, purpose="fine-tune")
    print("Validation file uploaded:", valid_file.id)

# --- Create fine-tuning job ---
job = client.fine_tuning.jobs.create(
    training_file=train_file.id,
    validation_file=valid_file.id if valid_file else None,
    model="gpt-4.1-2025-04-14",   # ✅ Supported for fine-tuning
    suffix="translation-ft",
)

print("Fine-tune job created:", job.id)

# --- Wait for completion ---
while True:
    job_status = client.fine_tuning.jobs.retrieve(job.id)
    print("Job status:", job_status.status)
    if job_status.status in ("succeeded", "failed", "cancelled"):
        break
    time.sleep(20)

if job_status.status == "succeeded":
    print("Fine-tuned model:", job_status.fine_tuned_model)
    # --- Run inference with the fine-tuned model ---
    resp = client.chat.completions.create(
        model=job_status.fine_tuned_model,
        messages=[{"role": "user", "content": "Translate to French: 'Good morning my friend'"}]
    )
    print("Response:", resp.choices[0].message.content)
else:
    print("Job did not succeed:", job_status.status)
