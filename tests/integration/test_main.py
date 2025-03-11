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


def test_provision_summary(s3_bucket):
    # Prepare test params
    params = {
        "organisation": "local-authority:BDG",
        "offset": 0,
        "limit": 8,
    }
    response = client.get("/performance/provision_summary", params=params)

    # Validate the results from the search
    assert response.status_code == 200

    response_data = response.json()
    assert "X-Pagination-Total-Results" in response.headers
    assert response.headers["X-Pagination-Total-Results"] == str(17)
    assert response.headers["X-Pagination-Limit"] == "8"

    assert len(response_data) > 0
    assert response_data[0]["dataset"] == "article-4-direction"
    for item in response_data:
        if item.get("dataset") == "article-4-direction-area":
            assert (
                item.get("active_endpoint_count") == 1
            ), "Expected active endpoint count to be 1"


def test_specification(s3_bucket):
    # Prepare test params
    params = {
        "offset": 0,
        "limit": 8,
    }

    response = client.get("/specification/specification", params=params)

    # Validate the results from the search
    assert response.status_code == 200

    response_data = response.json()
    assert "X-Pagination-Total-Results" in response.headers
    assert response.headers["X-Pagination-Total-Results"] == str(36)
    assert response.headers["X-Pagination-Limit"] == "8"

    assert len(response_data) > 0


def test_specification_with_dataset(s3_bucket):
    # Prepare test params
    params = {
        "offset": 0,
        "limit": 8,
        "dataset": "article-4-direction-area",
    }

    response = client.get("/specification/specification", params=params)

    # Validate the results from the search
    assert response.status_code == 200

    response_data = response.json()
    assert "X-Pagination-Total-Results" in response.headers
    assert response.headers["X-Pagination-Total-Results"] == str(1)
    assert response.headers["X-Pagination-Limit"] == "8"

    assert len(response_data) > 0
    assert response_data[0]["dataset"] == "article-4-direction-area"
    assert response_data[0]["fields"]
    assert len(response_data[0]["fields"]) > 1


def test_issue_type_summary(s3_bucket):
    # Prepare test params
    params = {
        "organisation": "local-authority:BUC",
        "dataset": "brownfield-land",
        "offset": 0,
        "limit": 8,
    }
    response = client.get("/performance/issue_type_summary", params=params)

    # Validate the results from the search
    assert response.status_code == 200

    response_data = response.json()
    assert "X-Pagination-Total-Results" in response.headers
    assert response.headers["X-Pagination-Total-Results"] == str(11)
    assert response.headers["X-Pagination-Limit"] == "8"
    assert len(response_data) > 0
    filtered_rows = [
        item
        for item in response_data
        if item.get("resource")
        == "8c61c7b72902daeaaa462002e62d840ce3916defacd54db97986654b180ce250"
    ]

    assert len(filtered_rows) == 6
    assert sum(1 for item in filtered_rows if item.get("issue_type") == "patch") == 4
    assert (
        sum(
            item.get("count_issues")
            for item in filtered_rows
            if item.get("issue_type") == "patch"
        )
        == 807
    )


def test_dataset_resource_mapping(s3_bucket):
    # Prepare test params
    params = {
        "organisation": "local-authority:BUC",
        "dataset": "article-4-direction-area",
        "offset": 0,
        "limit": 8,
    }
    response = client.get("/performance/dataset_resource_mapping", params=params)

    # Validate the results from the search
    assert response.status_code == 200

    response_data = response.json()
    assert "X-Pagination-Total-Results" in response.headers
    assert response.headers["X-Pagination-Total-Results"] == str(9)
    assert response.headers["X-Pagination-Limit"] == "8"
    assert len(response_data) > 0
    assert response_data[0]["mapping_field"] == "geometry"
    assert (
        response_data[0]["non_mapping_field"]
        == "start-date;entry-date;name;description;reference"
    )


def test_endpoint_dataset_summary(s3_bucket):
    # Prepare test params
    params = {
        "organisation": "local-authority:BUC",
        "dataset": "article-4-direction-area",
        "offset": 0,
        "limit": 10,
    }
    response = client.get("/performance/endpoint_dataset_summary", params=params)

    # Validate the results from the search
    assert response.status_code == 200

    response_data = response.json()
    assert "X-Pagination-Total-Results" in response.headers
    assert response.headers["X-Pagination-Total-Results"] == str(7)
    assert response.headers["X-Pagination-Limit"] == "10"
    assert len(response_data) > 0
    assert (
        response_data[0]["endpoint"]
        == "01de81578391eab3a1fdc9fcb92e559aa0a0bf1aafc777905d680fc0e189811e"
    )
