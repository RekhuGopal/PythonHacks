import boto3
import time
from botocore.exceptions import ClientError

region = "us-east-2"
bucket_name = "my-table-bucket-demo-12345"
namespace = "analytics_ns"
table_name = "employee_table"
athena_output = "s3://my-athena-query-results-bucket/results/"

s3tables = boto3.client("s3tables", region_name=region)
athena = boto3.client("athena", region_name=region)


# --------------------------------------------------------
# Utility: Wait for Athena query to complete
# --------------------------------------------------------
def wait_for_athena(query_id):
    while True:
        result = athena.get_query_execution(QueryExecutionId=query_id)
        state = result["QueryExecution"]["Status"]["State"]

        if state in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            return state

        time.sleep(2)


# --------------------------------------------------------
# CREATE TABLE BUCKET
# --------------------------------------------------------
def create_table_bucket(bucket_name):
    resp = s3tables.create_table_bucket(
        name=bucket_name,
        encryptionConfiguration={"sseAlgorithm": "AES256"},
    )
    print("Table Bucket Created:", resp["arn"])
    return resp["arn"]


# --------------------------------------------------------
# CREATE NAMESPACE
# --------------------------------------------------------
def create_namespace(bucket_arn, namespace):
    s3tables.create_namespace(
        tableBucketARN=bucket_arn,
        namespace=[namespace]
    )
    print("Namespace created:", namespace)


# --------------------------------------------------------
# CREATE TABLE
# --------------------------------------------------------
def create_table(bucket_arn, namespace, table_name):
    schema = {
        "iceberg": {
            "schema": {
                "fields": [
                    {"id": 1, "name": "id", "required": True, "type": "int"},
                    {"id": 2, "name": "name", "required": False, "type": "string"},
                    {"id": 3, "name": "role", "required": False, "type": "string"}
                ]
            }
        }
    }

    resp = s3tables.create_table(
        tableBucketARN=bucket_arn,
        namespace=namespace,
        name=table_name,
        format="ICEBERG",
        metadata=schema
    )
    print("Table ARN:", resp["tableARN"])
    return resp


# --------------------------------------------------------
# ATHENA DML: INSERT ROW
# --------------------------------------------------------
def insert_row(namespace, table_name, id, name, role):
    query = f"""
        INSERT INTO "{namespace}"."{table_name}"
        VALUES ({id}, '{name}', '{role}');
    """
    res = athena.start_query_execution(
        QueryString=query,
        ResultConfiguration={"OutputLocation": athena_output}
    )
    status = wait_for_athena(res["QueryExecutionId"])
    print("INSERT Status:", status)


# --------------------------------------------------------
# ATHENA SELECT (READ)
# --------------------------------------------------------
def read_rows(namespace, table_name):
    query = f'SELECT * FROM "{namespace}"."{table_name}"'
    res = athena.start_query_execution(
        QueryString=query,
        ResultConfiguration={"OutputLocation": athena_output}
    )
    wait_for_athena(res["QueryExecutionId"])
    result = athena.get_query_results(QueryExecutionId=res["QueryExecutionId"])
    print("Rows:")
    for row in result["ResultSet"]["Rows"]:
        print(row)


# --------------------------------------------------------
# ATHENA UPDATE (Iceberg MERGE)
# --------------------------------------------------------
def update_row(namespace, table_name, id, new_role):
    query = f"""
        MERGE INTO "{namespace}"."{table_name}" t
        USING (SELECT {id} AS id, '{new_role}' AS new_role) s
        ON t.id = s.id
        WHEN MATCHED THEN UPDATE SET role = s.new_role;
    """
    res = athena.start_query_execution(
        QueryString=query,
        ResultConfiguration={"OutputLocation": athena_output}
    )
    status = wait_for_athena(res["QueryExecutionId"])
    print("UPDATE Status:", status)


# --------------------------------------------------------
# ATHENA DELETE ROW
# --------------------------------------------------------
def delete_row(namespace, table_name, id):
    query = f"""
        DELETE FROM "{namespace}"."{table_name}"
        WHERE id = {id};
    """
    res = athena.start_query_execution(
        QueryString=query,
        ResultConfiguration={"OutputLocation": athena_output}
    )
    status = wait_for_athena(res["QueryExecutionId"])
    print("DELETE Status:", status)


# --------------------------------------------------------
# DELETE TABLE BUCKET (cleanup)
# --------------------------------------------------------
def delete_table_bucket(bucket_name):
    s3tables.delete_table_bucket(name=bucket_name)
    print("Deleted table bucket:", bucket_name)


# ========================================================
# MAIN WORKFLOW
# ========================================================
if __name__ == "__main__":

    # 1. Create Table Bucket
    bucket_arn = create_table_bucket(bucket_name)

    # 2. Create Namespace
    create_namespace(bucket_arn, namespace)

    # 3. Create Iceberg Table
    create_table(bucket_arn, namespace, table_name)

    # 4. INSERT Data
    insert_row(namespace, table_name, 1, "Alice", "DevOps Engineer")
    insert_row(namespace, table_name, 2, "Bob", "Cloud Architect")

    # 5. READ Data
    read_rows(namespace, table_name)

    # 6. UPDATE Data
    update_row(namespace, table_name, 1, "Principal DevOps Engineer")

    # 7. READ After Update
    read_rows(namespace, table_name)

    # 8. DELETE Data
    delete_row(namespace, table_name, 2)

    # 9. READ After Delete
    read_rows(namespace, table_name)

    # 10. Cleanup (optional)
    # delete_table_bucket(bucket_name)