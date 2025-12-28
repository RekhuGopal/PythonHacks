def aws_check_if_expected_buckets_exist(expected_bucket_count: int,s3_client,NoCredentialsError,ClientError) -> bool:
    """
    Checks if exactly `expected_bucket_count` S3 buckets exist
    in the AWS account accessible via OIDC credentials.

    Returns True if bucket count == expected_bucket_count, else False.
    """

    try:
        
        response = s3_client.list_buckets()
        buckets = response.get("Buckets", [])

        bucket_count = len(buckets)
        print(f"S3 bucket count in account: {bucket_count}")

        return bucket_count > expected_bucket_count

    except NoCredentialsError:
        print("AWS credentials not found. Ensure OIDC authentication via Service Connection.")
        return False

    except ClientError as e:
        print(f"AWS ClientError while listing S3 buckets: {e}")
        return False

    except Exception as e:
        print(f"Unexpected exception while counting S3 buckets: {e}")
        return False
