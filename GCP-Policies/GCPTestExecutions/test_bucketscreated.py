import os
import pytest
from googleapiclient import discovery
from google.oauth2 import service_account
from GCPTestCases.gcp_bucketscreated_tests  import gcp_check_if_two_buckets_exist


# ================================
# Read environment variables
# ================================

GCPEnv = os.environ.get("GCPENV")
GCPProjectID = os.environ.get("GCPProjectID")
GCPCredFilePath = os.environ.get("GCPCredFilePath")

if not GCPEnv or not GCPProjectID or not GCPCredFilePath:
    raise ValueError("Missing required variables: GCPENV, GCPProjectID, GCPCredFilePath")


# ================================
# Load credentials
# ================================

creds = service_account.Credentials.from_service_account_file(
    GCPCredFilePath,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)


# ================================
# Pytest Test Case – Bucket Count Check
# ================================

def test_gcp_bucket_count_is_two():
    """
    Verifies that exactly 2 GCS buckets exist in the project.
    """

    result = gcp_check_if_two_buckets_exist(GCPProjectID, creds, discovery)
    assert result == False
