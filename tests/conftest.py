import pytest
import duckdb
import os
import boto3
from moto import mock_aws
from botocore.exceptions import ClientError




os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_SECURITY_TOKEN"] = "testing"
os.environ["AWS_SESSION_TOKEN"] = "testing"
os.environ["COLLECTION_BUCKET"] = "test-bucket"
os.environ["ISSUES_BASE_PATH"] = "test/path"
os.environ["USE_AWS_CREDENTIAL_CHAIN"] = "false"




@pytest.fixture(scope="module")
def duckdb_connection():
    """
    Fixture to provide a DuckDB in-memory database connection.
    """
    conn = duckdb.connect(":memory:")  # In-memory database for testing
    conn.execute(f"SET s3_endpoint = 'localstack:4566';")
    conn.execute(f"SET s3_access_key_id = '{os.getenv('AWS_ACCESS_KEY_ID')}';")
    conn.execute(f"SET s3_secret_access_key = '{os.getenv('AWS_SECRET_ACCESS_KEY')}';")
    conn.execute(f"SET s3_region = '{os.getenv('AWS_DEFAULT_REGION')}';")
    conn.execute("SET s3_use_ssl=false;")
    conn.execute("SET s3_url_style = 'path';")
    yield conn
    conn.close()  



@pytest.fixture(scope="module")
def s3_client():
    """
    Fixture to provide an S3 client connected to LocalStack.
    """
    # Create an S3 client with the LocalStack endpoint
    s3 = boto3.client(
        "s3",
        endpoint_url="http://localstack:4566",  # LocalStack S3 endpoint
        region_name=os.environ["AWS_DEFAULT_REGION"],
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    )
    return s3


@pytest.fixture(scope="module")
def s3_bucket(s3_client):
    """
    Fixture to set up a test bucket and upload a Parquet file in LocalStack.
    """
    bucket_name = os.environ["COLLECTION_BUCKET"]
    parquet_file = "tests/files/issues.parquet"

    # Check if the bucket exists
    existing_buckets = s3_client.list_buckets().get("Buckets", [])
    if not any(bucket["Name"] == bucket_name for bucket in existing_buckets):
        # Create the bucket if it doesn't exist
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": os.environ["AWS_DEFAULT_REGION"]},
        )

    # Delete any pre-existing objects in the bucket
    objects = s3_client.list_objects_v2(Bucket=bucket_name).get("Contents", [])
    for obj in objects:
        s3_client.delete_object(Bucket=bucket_name, Key=obj["Key"])

    # Upload the Parquet file
    with open(parquet_file, "rb") as file:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f"{os.environ['ISSUES_BASE_PATH']}/issues.parquet",
            Body=file,
        )

    yield s3_client

@pytest.fixture
def s3_uri():
    """
    Fixture that provides the s3 URI for use in tests.
    """
    bucket_name = os.environ["COLLECTION_BUCKET"]
    base_path = os.environ["ISSUES_BASE_PATH"]
    s3_uri = f"s3://{bucket_name}/{base_path}/**/*.parquet"
    return s3_uri


