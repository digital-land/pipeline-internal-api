import os
import pytest
import duckdb
import boto3
from testcontainers.localstack import LocalStackContainer
from botocore.exceptions import ClientError


os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
os.environ["COLLECTION_BUCKET"] = "test-bucket"
os.environ["ISSUES_BASE_PATH"] = "test/path"
os.environ["PERFORMANCE_BASE_PATH"] = "test/path_perf"
os.environ["SPECIFICATION_BASE_PATH"] = "test/path_spec"
os.environ["USE_AWS_CREDENTIAL_CHAIN"] = "false"


@pytest.fixture(scope="module")
def localstack_container():
    # Start LocalStack container
    with LocalStackContainer() as localstack:
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
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )
    return s3


@pytest.fixture
def duckdb_connection(localstack_container):
    # Set up a DuckDB in-memory database
    conn = duckdb.connect()
    # Configure DuckDB to connect to S3 via LocalStack
    conn.execute(
        f"SET s3_endpoint = '{localstack_container.get_url().lstrip('http://')}';"  # noqa
    )
    conn.execute("SET s3_url_style = 'path';")
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
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                "LocationConstraint": os.environ["AWS_DEFAULT_REGION"]
            },
        )

    except ClientError:
        pass  # Ignore if bucket already exists

    # Upload a Parquet file to the bucket
    parquet_file = f"{test_dir}/../files/issues.parquet"
    with open(parquet_file, "rb") as f:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f"{os.environ['ISSUES_BASE_PATH']}/issues.parquet",
            Body=f,
        )

    parquet_file1 = f"{test_dir}/../files/provision_summary.parquet"
    with open(parquet_file1, "rb") as f:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f"{os.environ['PERFORMANCE_BASE_PATH']}/provision_summary.parquet",
            Body=f,
        )

    parquet_file2 = f"{test_dir}/../files/specification.parquet"
    with open(parquet_file2, "rb") as f:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f"{os.environ['SPECIFICATION_BASE_PATH']}/specification.parquet",
            Body=f,
        )

    yield s3_client
