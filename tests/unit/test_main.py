from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from pagination_model import PaginationParams, PaginatedResult

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


def mock_provision_summary(params):
    # Mocked data to simulate PaginatedResult
    return PaginatedResult(
        params=PaginationParams(offset=params.offset, limit=params.limit),
        total_results_available=2,
        data=[
            {
                "organisation": "development-corporation:Q105544651",
                "organisation_name": "Aycliffe and Peterlee Development Corporation",
                "dataset": "brownfield-site",
                "provision_reason": "prospective",
                "active_endpoint_count": 0,
                "error_endpoint_count": 0,
                "count_issue_error_internal": 0,
                "count_issue_error_external": 0,
                "count_issue_warning_internal": 0,
                "count_issue_warning_external": 0,
                "count_issue_notice_internal": 0,
                "count_issue_notice_external": 0,
            },
            {
                "organisation": "development-corporation:Q105544651",
                "organisation_name": "Aycliffe and Peterlee Development Corporation",
                "dataset": "developer-agreement",
                "provision_reason": "encouraged",
                "active_endpoint_count": 0,
                "error_endpoint_count": 0,
                "count_issue_error_internal": 0,
                "count_issue_error_external": 0,
                "count_issue_warning_internal": 0,
                "count_issue_warning_external": 0,
                "count_issue_notice_internal": 0,
                "count_issue_notice_external": 0,
            },
        ],
    )


def mock_dataset_issue_type_summary(params):
    # Mocked data to simulate PaginatedResult
    return PaginatedResult(
        params=PaginationParams(offset=params.offset, limit=params.limit),
        total_results_available=2,
        data=[
            {
                "organisation": "local-authority:ADU",
                "organisation_name": "Adur District Council",
                "cohort": "",
                "dataset": "brownfield-land",
                "collection": "brownfield-land",
                "pipeline": "brownfield-land",
                "endpoint": "ea98ea4d156ee47ff09af98d96d09951395b58e66d8b5fff55f50e3a537ff753",
                "endpoint_url": "https://www.adur-worthing.gov.uk/media/Media,146509,smxx.csv",
                "resource": "b5026e1fea560fab8479e7e551affd6aeb0d9423d09d562ce343cc8ee0194c71",
                "resource_start_date": "2024-06-05",
                "resource_end_date": "",
                "latest_log_entry_date": "2025-03-05",
                "count_issues": 51,
                "date": "05-03-2025",
                "issue_type": "OSGB",
                "severity": "warning",
                "responsibility": "external",
                "field": "GeoX,GeoY",
            },
            {
                "organisation": "local-authority:ADU",
                "organisation_name": "Adur District Council",
                "cohort": "",
                "dataset": "brownfield-land",
                "collection": "brownfield-land",
                "pipeline": "brownfield-land",
                "endpoint": "ea98ea4d156ee47ff09af98d96d09951395b58e66d8b5fff55f50e3a537ff753",
                "endpoint_url": "https://www.adur-worthing.gov.uk/media/Media,146509,smxx.csv",
                "resource": "b5026e1fea560fab8479e7e551affd6aeb0d9423d09d562ce343cc8ee0194c71",
                "resource_start_date": "2024-06-05",
                "resource_end_date": "",
                "latest_log_entry_date": "2025-03-05",
                "count_issues": 4,
                "date": "05-03-2025",
                "issue_type": "default-field",
                "severity": "info",
                "responsibility": "internal",
                "field": "LastUpdatedDate",
            },
        ],
    )


def mock_dataset_resource_summary(params):
    # Mocked data to simulate PaginatedResult
    return PaginatedResult(
        params=PaginationParams(offset=params.offset, limit=params.limit),
        total_results_available=2,
        data=[
            {
                "organisation": "local-authority:BST",
                "organisation_name": "Bristol City Council",
                "cohort": "ODP-Track4",
                "dataset": "tree-preservation-zone",
                "collection": "tree-preservation-order",
                "pipeline": "tree-preservation-zone",
                "endpoint": "e4c1a1851eb69c43ed4735aaa145d2975ef94f3a98ba7fe8ec30fa64dca7dba0",
                "endpoint_url": "https://maps2.bristol.gov.uk/MapServer/2/query?outFields=*&where=1%3D1&f=geojson",
                "resource": "5b81c3d12a06fcc4b6a2007eb3d9df857f704f3b4171af5d0588f3c24e633a9c",
                "resource_start_date": "2025-02-14",
                "resource_end_date": "",
                "latest_log_entry_date": "2025-02-25",
                "mapping_field": "geometry;reference;tree-preservation-order;tree-preservation-zone-type",
                "non_mapping_field": "SPECIES_1_NAME;SPECIES_2_NAME;SPECIES_3_NAME",
            },
            {
                "organisation": "local-authority:BUC",
                "organisation_name": "Buckinghamshire Council",
                "cohort": "RIPA-Beta",
                "dataset": "article-4-direction-area",
                "collection": "article-4-direction",
                "pipeline": "article-4-direction-area",
                "endpoint": "01de81578391eab3a1fdc9fcb92e559aa0a0bf1aafc777905d680fc0e189811e",
                "endpoint_url": "https://services7.arcgis.com//FeatureServer/0/query?where=1%3D1&f=geojson&outfields=*",
                "resource": "cf49bb0e4fe017644404d3991ab0bf34d1e723ab26853b76c0080057cf5e5376",
                "resource_start_date": "2024-10-03",
                "resource_end_date": "",
                "latest_log_entry_date": "2025-02-26",
                "mapping_field": "geometry",
                "non_mapping_field": "start-date;entry-date;name;description;reference",
            },
        ],
    )


def mock_endpoint_dataset_summary(params):
    # Mocked data to simulate PaginatedResult
    return PaginatedResult(
        params=PaginationParams(offset=params.offset, limit=params.limit),
        total_results_available=2,
        data=[
            {
                "organisation": "local-authority:BUC",
                "dataset": "article-4-direction-area",
                "endpoint": "cef4c02dacb006498d1c48729d2a18f3088b397132bce167e9b6c72f714b3a38",
                "endpoint_url": "https://services7.arcgis.com/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson",
                "resource": "090a4a90f160c121e491c1ddc3d7b4d232ecff0e4fe00f88bc9d38391b354cf4",
                "latest_status": "200",
                "latest_exception": "",
                "latest_log_entry_date": "2025-03-05",
                "entry_date": "2025-01-03",
                "end_date": "",
                "latest_resource_start_date": "2025-01-08",
                "resource_end_date": "",
            },
            {
                "organisation": "local-authority:BUC",
                "dataset": "brownfield-land",
                "endpoint": "776ad81957c21eaca97ecdb5b1434799a6ceaa0dd2d582e8b41c7c57c795c0dc",
                "endpoint_url": "https://buckinghamshire-gov-uk.s3.amazonaws.com/BC_Brownfield_Register_2024_3.csv",
                "resource": "8c61c7b72902daeaaa462002e62d840ce3916defacd54db97986654b180ce250",
                "latest_status": "200",
                "latest_exception": "",
                "latest_log_entry_date": "2025-03-05",
                "entry_date": "2025-01-07",
                "end_date": "",
                "latest_resource_start_date": "2025-01-14",
                "resource_end_date": "",
            },
        ],
    )


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


@patch("db.search_provision_summary", side_effect=mock_provision_summary)
def test_search_provision_summary(mock_provision_summary):
    # Test query params

    params = {
        "dataset": "brownfield-site",
        "offset": 0,
        "limit": 10,
    }
    response = client.get("/performance/provision_summary/", params=params)
    # Validate HTTP response
    assert response.status_code == 200

    # Validate headers
    assert response.headers["X-Pagination-Total-Results"] == "2"
    assert response.headers["X-Pagination-Offset"] == "0"
    assert response.headers["X-Pagination-Limit"] == "10"

    # Validate response data
    data = response.json()
    assert len(data) == 2
    assert data[0]["dataset"] == "brownfield-site"
    assert data[1]["active_endpoint_count"] == 0


@patch("db.search_issue_type_summary", side_effect=mock_dataset_issue_type_summary)
def test_search_issue_type_summary(mock_dataset_issue_type_summary):
    # Test query params

    params = {
        "dataset": "brownfield-land",
        "offset": 0,
        "limit": 10,
    }
    response = client.get("/performance/issue_type_summary/", params=params)
    # Validate HTTP response
    assert response.status_code == 200

    # Validate headers
    assert response.headers["X-Pagination-Total-Results"] == "2"
    assert response.headers["X-Pagination-Offset"] == "0"
    assert response.headers["X-Pagination-Limit"] == "10"

    # Validate response data
    data = response.json()
    assert len(data) == 2
    assert data[0]["dataset"] == "brownfield-land"
    assert data[1]["field"] == "LastUpdatedDate"


@patch("db.search_dataset_resource_mapping", side_effect=mock_dataset_resource_summary)
def test_search_dataset_resource_mapping(mock_dataset_resource_summary):
    # Test query params

    params = {
        "offset": 0,
        "limit": 10,
    }
    response = client.get("/performance/dataset_resource_mapping/", params=params)
    # Validate HTTP response
    assert response.status_code == 200

    # Validate headers
    assert response.headers["X-Pagination-Total-Results"] == "2"
    assert response.headers["X-Pagination-Offset"] == "0"
    assert response.headers["X-Pagination-Limit"] == "10"

    # Validate response data
    data = response.json()
    assert len(data) == 2
    assert data[0]["dataset"] == "tree-preservation-zone"
    assert (
        data[0]["mapping_field"]
        == "geometry;reference;tree-preservation-order;tree-preservation-zone-type"
    )


@patch("db.search_endpoint_dataset_summary", side_effect=mock_endpoint_dataset_summary)
def test_search_endpoint_dataset_summary(mock_endpoint_dataset_summary):
    # Test query params

    params = {
        "organisation": "local-authority:BUC",
        "offset": 0,
        "limit": 10,
    }
    response = client.get("/performance/endpoint_dataset_summary/", params=params)
    # Validate HTTP response
    assert response.status_code == 200

    # Validate headers
    assert response.headers["X-Pagination-Total-Results"] == "2"
    assert response.headers["X-Pagination-Offset"] == "0"
    assert response.headers["X-Pagination-Limit"] == "10"

    # Validate response data
    data = response.json()
    assert len(data) == 2
    assert data[0]["dataset"] == "article-4-direction-area"
    assert (
        data[1]["endpoint"]
        == "776ad81957c21eaca97ecdb5b1434799a6ceaa0dd2d582e8b41c7c57c795c0dc"
    )
