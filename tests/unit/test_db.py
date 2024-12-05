from unittest.mock import patch, MagicMock
from db import search_issues
from schema import IssuesParams
from pagination_model import PaginatedResult
import pytest


def test_search_issues():
    # Prepare test params
    params = IssuesParams(
        dataset="conservation-area",
        resource=None,
        field=None,
        issue_type=None,
        limit=10,
        offset=0,
    )

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

    # Mock `duckdb.connect`
    with patch("duckdb.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn

        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (mock_count,)
        mock_cursor.arrow.return_value.to_pylist.return_value = mock_results_data
        mock_conn.execute.return_value = mock_cursor

        result = search_issues(params)

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
