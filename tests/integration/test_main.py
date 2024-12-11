from fastapi.testclient import TestClient
from main import app
import json


# Create a test client for the FastAPI app
client = TestClient(app)


def test_search_issues(s3_bucket):
    # Prepare test params
    params = {
        "dataset": "conservation-area",
        "offset": 0,
        "limit": 10,
    }

    # Test the function that interacts with DuckDB and S3 via LocalStack
    response = client.get("/log/issue", params=params)

    # Validate the results from the search
    assert response.status_code == 200

    response_data = response.json()
    assert "X-Pagination-Total-Results" in response.headers
    assert response.headers["X-Pagination-Total-Results"] == str(83)

    assert len(response_data) > 0
    assert response_data[0]["dataset"] == "conservation-area"
    assert (
        response_data[0]["resource"]
        == "0b4284077da580a6daea59ee2227f9c7c55a9a45d57ef470d82418a4391ddf9a"
    )


def test_search_issues_no_parameters():
    # Prepare test params
    params = {}

    # Test the function that interacts with DuckDB and S3 via LocalStack
    response = client.get("/log/issue", params=params)

    response_json = json.loads(response.content.decode("utf-8"))
    details = response_json.get("detail", [])
    # Validate the results from the search
    assert response.status_code == 400
    assert any(
        "The 'dataset' query parameter is required" in detail for detail in details
    )
