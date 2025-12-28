import os
import pytest
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from AWSTestCases.aws_bucketscreated_tests import aws_check_if_expected_buckets_exist

# ================================
# Read environment variables
# ================================

AWSEnv = os.environ.get("ENV")
AWSRegion = os.environ.get("AWS_REGION")

if not AWSEnv or not AWSRegion:
    raise ValueError("Missing required variables: ENV, AWS_REGION")

s3_client = boto3.client("s3")

# ================================
# Pytest Test Case – Bucket Count Check
# ================================

def test_aws_bucket_count():
    """
    Verifies that exactly 3 S3 buckets exist in the AWS account.
    """

    expected_bucket_count = 3

    result = aws_check_if_expected_buckets_exist(expected_bucket_count, s3_client, NoCredentialsError, ClientError)
    assert result is False
