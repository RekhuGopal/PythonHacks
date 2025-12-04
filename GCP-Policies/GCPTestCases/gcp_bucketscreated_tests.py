def gcp_check_if_two_buckets_exist(project_id, creds, discovery):
    """
    Checks if exactly 2 GCS buckets exist in the project.
    Returns True if bucket count == 2, else False.
    """

    try:
        # Build Storage API client
        storage_client = discovery.build(
            "storage", "v1", credentials=creds, cache_discovery=False
        )

        # Fetch bucket list
        response = storage_client.buckets().list(project=project_id).execute()

        # Extract bucket names
        buckets = response.get("items", [])

        bucket_count = len(buckets)
        print(f"Bucket count in project {project_id}: {bucket_count}")

        return bucket_count == 3

    except Exception as e:
        print(f"Exception while counting GCS buckets: {e}")
        return False