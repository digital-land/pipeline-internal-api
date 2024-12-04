from fastapi.testclient import TestClient
import unittest
from unittest.mock import patch, MagicMock
from main import app
import os


# Create a test client for the FastAPI app
client = TestClient(app)



def test_search_issues_integration(s3_bucket, duckdb_connection):
    # Prepare test params
    params = {
        "dataset": "conservation-area",
        "offset": 0,
        "limit": 10,
    }
    
    with patch("db.duckdb.connect", return_value=duckdb_connection):
        response = client.get("/log/issue", params=params)
        
    # Validate the results from the search
    assert response.status_code == 200
    
    response_data = response.json()
    assert "X-Pagination-Total-Results" in response.headers
    assert response.headers["X-Pagination-Total-Results"] == str(83)

    assert len(response_data) > 0
    assert response_data[0]['dataset'] == 'conservation-area'  # Ensure the key exists in the data
    assert response_data[0]['resource'] == '0b4284077da580a6daea59ee2227f9c7c55a9a45d57ef470d82418a4391ddf9a'

def test_search_issues_no_parameters(s3_bucket, duckdb_connection):
    # Prepare test params
    params = {}
    
    
    with patch("db.duckdb.connect", return_value=duckdb_connection):
        response = client.get("/log/issue", params=params)
        
    # Validate the results from the search
    assert response.status_code == 400 #confirm from Chris (this should be 500)
