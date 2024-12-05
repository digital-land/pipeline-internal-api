from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from pagination_model import PaginationParams, PaginatedResult
import os

# Create a test client for the FastAPI app
client = TestClient(app)


def mock_search_issues(params):
    # Mocked data to simulate PaginatedResult
    return PaginatedResult(
        params=PaginationParams(offset=params.offset, limit=params.limit),
        total_results_available=2,
        data=[
            {
                "dataset": "ancient-woodland",
                "resource": "1d5336e3a650cb037328bf9c2911309328cdc743935842d7b6792484ccac7eca",
                "line-number": 549,
                "entry-number": 548,
                "field": "geometry",
                "issue-type": "invalid geometry - fixed",
                "value": "Too few points in geometry component[0.259555 50.936166]",
                "message": "None",
            },
            {
                "dataset": "ancient-woodland",
                "resource": "1d5336e3a650cb037328bf9c2911309328cdc743935842d7b6792484ccac7eca",
                "line-number": 934,
                "entry-number": 933,
                "field": "geometry",
                "issue-type": "invalid geometry - fixed",
                "value": "Ring Self-intersection[0.124675 51.139896]",
                "message": "None",
            },
        ],
    )


def test_bucket_and_file_existence(s3_client, s3_bucket):
    # Test if the bucket exists
    bucket_name = os.environ["COLLECTION_BUCKET"]
    buckets = s3_client.list_buckets()["Buckets"]
    bucket_names = [bucket["Name"] for bucket in buckets]
    assert bucket_name in bucket_names, f"Bucket {bucket_name} does not exist"

    # Test if the file exists in the bucket
    files = s3_client.list_objects(Bucket=bucket_name).get("Contents", [])
    file_keys = [file["Key"] for file in files]
    assert "test/path/issues.parquet" in file_keys, "File does not exist in the bucket"


def test_duckdb_query_with_localstack(s3_client, s3_bucket, duckdb_connection):
    # Query to fetch data from the Parquet file in S3
    query = f"SELECT * FROM 's3://{os.environ['COLLECTION_BUCKET']}/test/path/issues.parquet' LIMIT 10"
    # Execute the query and fetch results
    result = duckdb_connection.execute(query).fetchall()

    # Check if the result contains any rows
    assert len(result) > 0, "No rows returned from the S3 query"


@patch("db.search_issues", side_effect=mock_search_issues)
def test_issues_endpoint(mock_search_issues):
    # Test query params

    params = {
        "dataset": "ancient-woodland",
        "offset": 0,
        "limit": 10,
    }
    response = client.get("/log/issue/", params=params)
    # Validate HTTP response
    assert response.status_code == 200

    # Validate headers
    assert response.headers["X-Pagination-Total-Results"] == "2"
    assert response.headers["X-Pagination-Offset"] == "0"
    assert response.headers["X-Pagination-Limit"] == "10"

    # Validate response data
    data = response.json()
    assert len(data) == 2
    assert data[0]["dataset"] == "ancient-woodland"
    assert (
        data[1]["resource"]
        == "1d5336e3a650cb037328bf9c2911309328cdc743935842d7b6792484ccac7eca"
    )
