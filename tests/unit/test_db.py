import unittest
from unittest.mock import patch, MagicMock
from db import search_issues, _add_condition
from schema import IssuesParams
from pagination_model import PaginationParams, PaginatedResult
import os




def test_search_issues_integration(s3_bucket, duckdb_connection):
    # Prepare test params
    params = IssuesParams(
        dataset="conservation-area",
        resource=None,
        field=None,
        issue_type=None,
        limit=10,
        offset=0
    )
    
    # Test the function that interacts with DuckDB and S3 via LocalStack
    with patch("db.duckdb.connect", return_value=duckdb_connection):
        result = search_issues(params)
    
    # Validate the results from the search
    assert isinstance(result, PaginatedResult)
    assert len(result.data) > 0  # Check if we received data
    assert result.total_results_available == 83  # Expected result from the mocked S3 interaction
    assert result.data[0]['dataset'] == 'conservation-area'  # Ensure the key exists in the data
    assert result.data[0]['resource'] == '0b4284077da580a6daea59ee2227f9c7c55a9a45d57ef470d82418a4391ddf9a'

# def test_search_issues_no_conditions(s3_bucket, duckdb_connection):

#     # Test parameters
#     params = IssuesParams(
#         dataset=None,
#         resource=None,
#         field=None,
#         issue_type=None,
#         limit=5,
#         offset=0
#     )

#     s3_uri = f"s3://{os.environ['COLLECTION_BUCKET']}/{os.environ['ISSUES_BASE_PATH']}/**/*.parquet"

#     # Test the function that interacts with DuckDB and S3 via LocalStack
#     with patch("db.duckdb.connect", return_value=duckdb_connection):
#         result = search_issues(params)

#     # Validate the results from the search
#     assert isinstance(result, PaginatedResult)
#     assert result.total_results_available == 0
#     assert len(result.data) == 0

#     # def test_search_issues_success(self, mock_logger, mock_duckdb_connect, mock_environ):
#     #     # Mock environment variables
#     #     mock_environ.get.side_effect = lambda key, default: {
#     #         "COLLECTION_BUCKET": "test-bucket",
#     #         "ISSUES_BASE_PATH": "test/path",
#     #         "USE_AWS_CREDENTIAL_CHAIN": "false"
#     #     }.get(key, default)

#     #     # Mock DuckDB connection and results
#     #     mock_conn = MagicMock()
#     #     mock_duckdb_connect.return_value.__enter__.return_value = mock_conn

#     #     mock_conn.execute.return_value.fetchone.return_value = [42]  # Mock count
#     #     mock_conn.execute.return_value.arrow.return_value.to_pylist.return_value = [
#     #         {"dataset": "dataset1", "resource": "resource1"}
#     #     ]  # Mock data

#     #     # Test parameters
#     #     params = IssuesParams(
#     #         dataset="dataset1",
#     #         resource=None,
#     #         field=None,
#     #         issue_type=None,
#     #         limit=10,
#     #         offset=0
#     #     )

#     #     # Execute the function
#     #     result = search_issues(params)

#     #     # Assertions
#     #     self.assertIsInstance(result, PaginatedResult)
#     #     self.assertEqual(result.total_results_available, 42)
#     #     self.assertEqual(result.data, [{"dataset": "dataset1", "resource": "resource1"}])

#     #     # Assert SQL queries
#     #     mock_conn.execute.assert_any_call(
#     #         "SELECT COUNT(*) FROM 's3://test-bucket/test/path/**/*.parquet' WHERE dataset = 'dataset1' "
#     #     )
#     #     mock_conn.execute.assert_any_call(
#     #         "SELECT * FROM 's3://test-bucket/test/path/**/*.parquet' WHERE dataset = 'dataset1' LIMIT 10 OFFSET 0"
#     #     )


#     # def test_search_issues_no_conditions(self, mock_logger, mock_duckdb_connect, mock_environ):
#     #     # Mock environment variables
#     #     mock_environ.get.side_effect = lambda key, default: {
#     #         "COLLECTION_BUCKET": "test-bucket",
#     #         "ISSUES_BASE_PATH": "test/path",
#     #         "USE_AWS_CREDENTIAL_CHAIN": "false"
#     #     }.get(key, default)

#     #     # Mock DuckDB connection and results
#     #     mock_conn = MagicMock()
#     #     mock_duckdb_connect.return_value.__enter__.return_value = mock_conn

#     #     mock_conn.execute.return_value.fetchone.return_value = [0]  # Mock count
#     #     mock_conn.execute.return_value.arrow.return_value.to_pylist.return_value = []  # Mock data

#     #     # Test parameters
#     #     params = IssuesParams(
#     #         dataset=None,
#     #         resource=None,
#     #         field=None,
#     #         issue_type=None,
#     #         limit=5,
#     #         offset=0
#     #     )

#     #     # Execute the function
#     #     result = search_issues(params)

#     #     # Assertions
#     #     self.assertIsInstance(result, PaginatedResult)
#     #     self.assertEqual(result.total_results_available, 0)
#     #     self.assertEqual(result.data, [])

#     #     # Assert SQL queries
#     #     mock_conn.execute.assert_any_call(
#     #         "SELECT COUNT(*) FROM 's3://test-bucket/test/path/**/*.parquet' "
#     #     )
#     #     mock_conn.execute.assert_any_call(
#     #         "SELECT * FROM 's3://test-bucket/test/path/**/*.parquet' LIMIT 5 OFFSET 0"
#     #     )

#     # @patch("db.os.environ")
#     # @patch("db.duckdb.connect")
#     # @patch("db.logger")
#     # def test_search_issues_failure(self, mock_logger, mock_duckdb_connect, mock_environ):
#     #     # Mock environment variables
#     #     mock_environ.get.side_effect = lambda key, default: {
#     #         "COLLECTION_BUCKET": "test-bucket",
#     #         "ISSUES_BASE_PATH": "test/path",
#     #         "USE_AWS_CREDENTIAL_CHAIN": "false"
#     #     }.get(key, default)

#     #     # Mock DuckDB connection to raise an exception
#     #     mock_conn = MagicMock()
#     #     mock_duckdb_connect.return_value.__enter__.return_value = mock_conn
#     #     mock_conn.execute.side_effect = Exception("DuckDB Error")

#     #     # Test parameters
#     #     params = IssuesParams(
#     #         dataset=None,
#     #         resource=None,
#     #         field=None,
#     #         issue_type=None,
#     #         limit=10,
#     #         offset=0
#     #     )

#     #     # Execute the function and assert exception
#     #     with self.assertRaises(Exception) as context:
#     #         search_issues(params)

#     #     self.assertEqual(str(context.exception), "DuckDB Error")
#     #     mock_logger.exception.assert_called_with("Failure executing DuckDB queries")


