import os
import pytest
import duckdb
import boto3
from testcontainers.localstack import LocalStackContainer
from botocore.exceptions import ClientError


os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["COLLECTION_BUCKET"] = "test-bucket"
os.environ["ISSUES_BASE_PATH"] = "test/path"

@pytest.fixture(scope="module")
def localstack_container():
    # Start LocalStack container
    with LocalStackContainer(image="localstack/localstack:2.0.1") as localstack:
        # Wait for the service to be ready
        yield localstack

@pytest.fixture(scope="module")
def s3_client(localstack_container):
    # Create an S3 client using the LocalStack endpoint
    s3 = boto3.client(
        "s3",
        endpoint_url=localstack_container.get_url(),
        region_name=os.environ["AWS_DEFAULT_REGION"],
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
    )
    return s3

@pytest.fixture(scope="module")
def duckdb_connection(localstack_container):
    
    with LocalStackContainer() as localstack:
        localstack_hostname = localstack.get_container_host_ip()
    # Set up a DuckDB in-memory database
    conn = duckdb.connect(":memory:")
    # Configure DuckDB to connect to S3 via LocalStack
    conn.execute(f"SET s3_endpoint = '{localstack_hostname}:{4566}';")
    conn.execute(f"SET s3_access_key_id = '{os.getenv('AWS_ACCESS_KEY_ID')}';")
    conn.execute(f"SET s3_secret_access_key = '{os.getenv('AWS_SECRET_ACCESS_KEY')}';")
    conn.execute(f"SET s3_region = '{os.getenv('AWS_DEFAULT_REGION')}';")
    conn.execute("SET s3_use_ssl = FALSE;")
    yield conn
    conn.close()


@pytest.fixture(scope="module")
def test_dir(request):
    return os.path.dirname(request.module.__file__)


@pytest.fixture(scope="module")
def s3_bucket(s3_client, test_dir):
    # Create a bucket in LocalStack for the test
    bucket_name = os.environ["COLLECTION_BUCKET"]
    try:
        s3_client.create_bucket(Bucket=bucket_name)
    except ClientError:
        pass  # Ignore if bucket already exists

    # Upload a Parquet file to the bucket
    parquet_file = f"{test_dir}/../files/issues.parquet"
    with open(parquet_file, "rb") as f:
        s3_client.put_object(Bucket=bucket_name, Key="test/path/issues.parquet", Body=f)
    
    yield s3_client
