import boto3
import json
import time

# ---- CONFIG ----
region = "us-west-2"  # Ensure this is the correct region
bucket_name = "bedrock-video-generation-us-west-2-anmpoa"  # Replace with your S3 bucket name
s3_prefix = "luma-videos"  # Folder inside your bucket
prompt = "A futuristic city skyline with flying cars at sunset"

# Bedrock + S3 clients
bedrock = boto3.client("bedrock-runtime", region_name=region)
s3 = boto3.client("s3", region_name=region)

def invoke_luma_ray(prompt, bucket, prefix):
    """Start async text-to-video job with Luma Ray v2"""
    model_id = "luma.ray-v2:0"

    # Define the model input structure
    model_input = {
        "prompt": prompt,
        "duration": "5s",
        "resolution": "720p",
        "aspect_ratio": "16:9"
    }

    # Define the output data configuration
    output_data_config = {
        "s3OutputDataConfig": {
            "s3Uri": f"s3://{bucket}/{prefix}/"
        }
    }

    # Start the asynchronous invocation
    response = bedrock.start_async_invoke(
        modelId=model_id,
        modelInput=model_input,
        outputDataConfig=output_data_config
    )
    return response["invocationArn"]

def wait_for_job(invocation_arn):
    """Poll until async job finishes"""
    while True:
        status_resp = bedrock.get_async_invoke(
            invocationArn=invocation_arn
        )
        status = status_resp["status"]
        print(f"Job status: {status}")

        if status in ["Completed", "FAILED"]:
            return status_resp
        time.sleep(15)

def get_presigned_url(bucket, key, expiry=3600):
    """Generate presigned URL for S3 object"""
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expiry
    )

def text_to_video(prompt, bucket, prefix):
    # Step 1: Start async job
    invocation_arn = invoke_luma_ray(prompt, bucket, prefix)
    print(f"Started job: {invocation_arn}")

    # Step 2: Wait until job completes
    result = wait_for_job(invocation_arn)

    if result["status"] == "FAILED":
        raise RuntimeError("Video generation failed")

    # Step 3: Extract S3 output location
    output_uri = result["outputDataConfig"]["s3OutputDataConfig"]["s3Uri"]
    # Example: s3://bucket/prefix/jobid/output.mp4
    parts = output_uri.replace("s3://", "").split("/", 1)
    bucket_name = parts[0]
    key_prefix = parts[1]

    # We don’t know the exact file name upfront, list objects
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=key_prefix)
    for obj in response.get("Contents", []):
        if obj["Key"].endswith(".mp4"):
            presigned = get_presigned_url(bucket_name, obj["Key"])
            return presigned

    raise FileNotFoundError("No MP4 video found in output folder")

# ---- RUN ----
if __name__ == "__main__":
    url = text_to_video(prompt, bucket_name, s3_prefix)
    print(f"\n✅ Video ready: {url}")