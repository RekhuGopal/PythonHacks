import boto3
import json
import time
import botocore.exceptions

# ---- CONFIG ----
REGION = "us-west-2"
BUCKET_NAME = "bedrock-video-generation-us-west-2-anmpoa"   # Replace with your S3 bucket
S3_PREFIX = "luma-videos"          # Folder inside bucket
VIDEO_DURATION = "5s"
VIDEO_RESOLUTION = "720p"
MAX_RETRIES = 5                     # Max retries on throttling
POLL_INTERVAL = 15                  # seconds

# Clients
bedrock = boto3.client("bedrock-runtime", region_name=REGION)
s3 = boto3.client("s3", region_name=REGION)


def invoke_luma_ray(prompt, bucket, prefix, max_retries=MAX_RETRIES):
    """Start async Luma Ray v2 job with exponential backoff on throttling."""
    model_id = "luma.ray-v2:0"
    model_input = {
        "prompt": prompt,
        "duration": VIDEO_DURATION,
        "resolution": VIDEO_RESOLUTION,
        "aspect_ratio": "16:9"
    }
    output_data_config = {
        "s3OutputDataConfig": {
            "s3Uri": f"s3://{bucket}/{prefix}/"
        }
    }

    delay = 2
    for attempt in range(max_retries):
        try:
            response = bedrock.start_async_invoke(
                modelId=model_id,
                modelInput=model_input,
                outputDataConfig=output_data_config
            )
            print(f"[Bedrock] Job started successfully on attempt {attempt + 1}")
            return response["invocationArn"]
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "ThrottlingException":
                print(f"[Bedrock] Throttled, retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2  # exponential backoff
            else:
                raise
    raise RuntimeError(f"[Bedrock] Failed to start job after {max_retries} retries due to throttling")


def wait_for_job(invocation_arn, poll_interval=POLL_INTERVAL):
    """Poll until async job finishes"""
    while True:
        resp = bedrock.get_async_invoke(invocationArn=invocation_arn)
        status = resp["status"]
        print(f"[Bedrock] Job status: {status}")

        if status == "Completed":
            return resp
        elif status == "FAILED":
            raise RuntimeError(f"[Bedrock] Video generation failed: {resp}")
        time.sleep(poll_interval)


def get_presigned_url(bucket, key, expiry=3600):
    """Generate presigned S3 URL."""
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expiry
    )


def lambda_handler(event, context):
    """
    Lambda handler for Bedrock Luma Ray text-to-video.
    Expects JSON event: {"prompt": "your prompt here"}
    """
    prompt = event.get("prompt")
    if not prompt:
        return {"statusCode": 400, "body": "Missing 'prompt' in request"}

    # Step 1: Start async job with throttling handling
    invocation_arn = invoke_luma_ray(prompt, BUCKET_NAME, S3_PREFIX)
    print(f"[Bedrock] Started job: {invocation_arn}")

    # Step 2: Wait for job completion (blocking)
    result = wait_for_job(invocation_arn)

    # Step 3: Extract S3 output URI
    output_uri = result["outputDataConfig"]["s3OutputDataConfig"]["s3Uri"]
    parts = output_uri.replace("s3://", "").split("/", 1)
    bucket_name = parts[0]
    key_prefix = parts[1]

    # Step 4: List S3 objects and find MP4 file
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=key_prefix)
    video_url = None
    for obj in response.get("Contents", []):
        if obj["Key"].endswith(".mp4"):
            video_url = get_presigned_url(bucket_name, obj["Key"])
            break

    if not video_url:
        return {"statusCode": 500, "body": "No MP4 video found in output folder"}

    return {"statusCode": 200, "videoUrl": video_url}