from unittest.mock import patch, MagicMock
from db import (
    search_issues,
    duck_db_connection,
    search_provision_summary,
    search_issue_type_summary,
    search_dataset_resource_mapping,
    search_endpoint_dataset_summary,
    get_specification,
)
from schema import (
    IssuesParams,
    IssueTypeSummaryParams,
    CommonParams,
    SpecificationsParams,
)
from pagination_model import PaginatedResult
import pytest
import json

# Mock data
mock_results_data = [
    {
        "dataset": "conservation-area",
        "resource": "0b4284077da580a6daea59ee2227f9c7c55a9a45d57ef470d82418a4391ddf9a",
    },
    {
        "dataset": "conservation-area",
        "resource": "test",
    },
]
mock_count = 2


@pytest.fixture
def sample_query_params():
    return ["sample_value"]


@pytest.fixture
def sample_sql_count():
    return "SELECT COUNT(*) FROM sample_table WHERE column = ?"


@pytest.fixture
def sample_sql_results():
    return "SELECT * FROM sample_table WHERE column = ? LIMIT ? OFFSET ?"


@pytest.fixture
def sample_issue_params():
    return IssuesParams(
        dataset="sample_dataset",
        resource="abc123",
        field="geometry",
        issue_type="sample_issue",
        limit=10,
        offset=0,
    )


@pytest.fixture
def sample_issue_type_params():
    return IssueTypeSummaryParams(
        dataset="sample_dataset",
        organisation="sample_org",
        issueType="sample_issue",
        issueField=None,
        severity=None,
        responsibility=None,
        limit=10,
        offset=0,
    )


@pytest.fixture
def sample_common_params():
    return CommonParams(
        dataset="sample_dataset", organisation="sample_org", limit=10, offset=0
    )


@pytest.fixture
def sample_specification_params():
    return SpecificationsParams(dataset="sample_dataset", limit=10, offset=0)


@patch("duckdb.connect")
def test_search_issues(mock_connect, sample_issue_params):
    # Mock `duckdb.connect`

    mock_conn = MagicMock()
    mock_connect.return_value.__enter__.return_value = mock_conn

    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (mock_count,)
    mock_cursor.arrow.return_value.to_pylist.return_value = mock_results_data
    mock_conn.execute.return_value = mock_cursor

    result = search_issues(sample_issue_params)

    # Validate the results from the search
    assert isinstance(result, PaginatedResult)
    assert len(result.data) == 2  # Check if we received data
    assert (
        result.total_results_available == 2
    )  # Expected result from the mocked S3 interaction
    assert (
        result.data[0]["dataset"] == "conservation-area"
    )  # Ensure the key exists in the data
    assert (
        result.data[0]["resource"]
        == "0b4284077da580a6daea59ee2227f9c7c55a9a45d57ef470d82418a4391ddf9a"
    )


def test_search_issues_no_dataset():
    # Expect the validation error when dataset is None
    with pytest.raises(ValueError, match="The 'dataset' query parameter is required."):
        IssuesParams(
            dataset=None, resource=None, field=None, issue_type=None, limit=10, offset=0
        )


@patch("duckdb.connect")
def test_search_provision_summary(mock_connect, sample_common_params):
    """Test search_issue_type_summary with mocked DuckDB connection."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Mock query results
    mock_cursor.fetchone.return_value = [5]  # Simulated COUNT(*) result
    mock_cursor.arrow.return_value.to_pylist.return_value = [
        {
            "organisation": "org1",
            "dataset": "data1",
            "active_endpoint_count": 0,
            "error_endpoint_count": 0,
        },
        {
            "organisation": "org2",
            "dataset": "data2",
            "active_endpoint_count": 4,
            "error_endpoint_count": 1,
        },
        {
            "organisation": "org3",
            "dataset": "data3",
            "active_endpoint_count": 5,
            "error_endpoint_count": 3,
        },
    ]

    mock_conn.execute.return_value = mock_cursor
    mock_connect.return_value.__enter__.return_value = mock_conn

    result = search_provision_summary(sample_common_params)

    assert isinstance(result, PaginatedResult)
    assert result.total_results_available == 5
    assert len(result.data) == 3
    assert result.data[0]["organisation"] == "org1"


@patch("duckdb.connect")
def test_search_issue_type_summary(mock_connect, sample_issue_type_params):
    """Test search_issue_type_summary with mocked DuckDB connection."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Mock query results
    mock_cursor.fetchone.return_value = [5]  # Simulated COUNT(*) result
    mock_cursor.arrow.return_value.to_pylist.return_value = [
        {
            "organisation": "org1",
            "dataset": "data1",
            "issue_type": "type1",
            "field": "field1",
        },
        {
            "organisation": "org2",
            "dataset": "data2",
            "issue_type": "type2",
            "field": "field2",
        },
    ]

    mock_conn.execute.return_value = mock_cursor
    mock_connect.return_value.__enter__.return_value = mock_conn

    result = search_issue_type_summary(sample_issue_type_params)

    assert isinstance(result, PaginatedResult)
    assert result.total_results_available == 5
    assert len(result.data) == 2
    assert result.data[0]["issue_type"] == "type1"


@patch("duckdb.connect")
def test_search_dataset_resource_mapping(mock_connect, sample_common_params):
    """Test search_dataset_resource_mapping with mocked DuckDB connection."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = [3]  # Simulated COUNT(*) result
    mock_cursor.arrow.return_value.to_pylist.return_value = [
        {"dataset": "data1", "resource": "res1"},
        {"dataset": "data2", "resource": "res2"},
    ]

    mock_conn.execute.return_value = mock_cursor
    mock_connect.return_value.__enter__.return_value = mock_conn

    result = search_dataset_resource_mapping(sample_common_params)

    assert isinstance(result, PaginatedResult)
    assert result.total_results_available == 3
    assert len(result.data) == 2
    assert result.data[1]["dataset"] == "data2"


@patch("duckdb.connect")
def test_search_endpoint_dataset_summary(mock_connect, sample_common_params):
    """Test search_endpoint_dataset_summary with mocked DuckDB connection."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = [8]  # Simulated COUNT(*) result
    mock_cursor.arrow.return_value.to_pylist.return_value = [
        {"dataset": "data1", "endpoint": "endpoint1"},
        {"dataset": "data2", "endpoint": "endpoint2"},
    ]

    mock_conn.execute.return_value = mock_cursor
    mock_connect.return_value.__enter__.return_value = mock_conn

    result = search_endpoint_dataset_summary(sample_common_params)

    assert isinstance(result, PaginatedResult)
    assert result.total_results_available == 8
    assert len(result.data) == 2
    assert result.data[0]["endpoint"] == "endpoint1"


@patch("duckdb.connect")
def test_get_specification(mock_connect, sample_specification_params, caplog):
    """Test get_specification with mocked DuckDB connection."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Mock COUNT(*) result
    mock_cursor.fetchone.return_value = [3]

    # Mock JSON data results
    mock_cursor.arrow.return_value.to_pylist.return_value = [
        {"json": json.dumps({"dataset": "test_dataset", "spec": "value1"})},
        {"json": json.dumps({"dataset": "test_dataset", "spec": "value2"})},
    ]

    mock_conn.execute.return_value = mock_cursor
    mock_connect.return_value.__enter__.return_value = mock_conn

    result = get_specification(sample_specification_params)

    # Assertions on return value
    assert isinstance(result, PaginatedResult)
    assert result.total_results_available == 3
    assert len(result.data) == 2
    assert result.data[0]["dataset"] == "test_dataset"
    assert result.data[1]["spec"] == "value2"


@patch("duckdb.connect")
def test_duck_db_connection_exception(
    mock_connect,
    sample_issue_params,
    sample_query_params,
    sample_sql_count,
    sample_sql_results,
):
    mock_conn = MagicMock()
    mock_conn.execute.side_effect = Exception("Database error")  # Simulate an error

    mock_connect.return_value.__enter__.return_value = mock_conn

    with pytest.raises(Exception, match="Database error"):
        duck_db_connection(
            sample_issue_params,
            sample_query_params,
            sample_sql_count,
            sample_sql_results,
        )
