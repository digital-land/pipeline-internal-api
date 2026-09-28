# pipeline-api
Publicly internal API providing access to data pipeline metadata.

Implemented in Python using Fast API.  DuckDB is used to read from Parquet files hosted on S3.

## Requirements

The minimum requirements for building and running locally are:

 * Docker
 * Docker Compose

In order to build and test the software outside of Docker, you will need

 * Make
 * Python (version as per .python-version)

## Running locally with docker compose

You can run the API locally by running either `make compose-up` or `docker compose up -d --build`.

The docker compose setup runs the S3 locally using Localstack as well as the API.  An S3 bucket called local-collection-data is created and seeded with example files in the collection-data directory.


## Tests

With your virtual environment activated (see [Local setup](#local-setup)), install the dependencies:

```
make init
```

Then run the linters, unit tests and integration tests:

```
make test
```

The integration tests start a LocalStack container, so Docker needs to be running.


## Maintenance and upgrading

### Local setup

Create a virtual environment using the Python version in `.python-version` (pyenv will pick this up automatically) and install the dependencies:

```
python -m venv .venv
source .venv/bin/activate
make init
```

### Python dependencies

Dependencies are managed with [pip-tools](https://github.com/jazzband/pip-tools):

 * `requirements/requirements.in` and `requirements/test_requirements.in` list the direct dependencies, without pinned versions
 * `requirements/requirements.txt` and `requirements/test_requirements.txt` are generated lock files with every package pinned. Don't edit these by hand

To upgrade all packages to their latest versions, run:

```
make upgrade
```

This regenerates both lock files and installs the new versions into your virtual environment. It fails if the active Python doesn't match `.python-version`, because the lock files are resolved for a specific Python version.

To upgrade a single package, run:

```
pip-compile --upgrade-package duckdb requirements/requirements.in
pip-compile requirements/test_requirements.in
```

Run `make test` after upgrading, and review the changes to the lock files before committing.

### Debian packages

The Docker image runs `apt-get upgrade` at build time so that it picks up Debian security updates (for example, OpenSSL). These packages aren't pinned, so rebuild the image regularly to stay patched.

### Upgrading Python

To move to a new Python version, change all of the following together:

 * `.python-version`
 * the base image in `Dockerfile` (e.g. `python:3.13-slim-bookworm`)
 * the lock files, by recreating your virtual environment on the new version and running `make upgrade`


## Swagger UI

The Swagger UI bundled with Fast API is a useful way to explore the API and try out the endpoints.  It's exposed on the /docs path, e.g.

http://localhost:8000/docs


## S3 Data Sources

All endpoints read from the `production-collection-data` S3 bucket (configurable via `COLLECTION_BUCKET`):

| Endpoint | S3 Path |
|---|---|
| `/log/issue` | `log/issue/**/*.parquet` |
| `/performance/provision_summary` | `data/performance/provision_summary.parquet` |
| `/performance/issue_type_summary` | `data/performance/endpoint_dataset_issue_type_summary.parquet` |
| `/performance/dataset_resource_mapping` | `data/performance/endpoint_dataset_resource_summary.parquet` |
| `/performance/endpoint_dataset_summary` | `data/performance/endpoint_dataset_summary.parquet` |
| `/specification/specification` | `data/specification/*.parquet` |


## Endpoints

### /log/issue

S3 path: `log/issue/**/*.parquet`

The /log/issue path exposes issue logs in a paginated result style.  Offset and limit query parameters control the page of results you want to obtain while the X-Pagination-* headers provide the context for where you are within the result set as well as the total results available.

Optional Parameters:
 * `offset`
 * `limit`
 * `dataset` (required)
 * `resource`
 * `field`
 * `issue_type`

Most basic request:

```
curl http://localhost:8000/log/issue
```

Basic request with pagination:

```
curl http://localhost:8000/log/issue?offset=50&limit=50
```

Request for ancient-woodland issues:

```
http://localhost:8000/log/issue?dataset=ancient-woodland
```

Request for ancient-woodland issues with pagination:

```
http://localhost:8000/log/issue?dataset=ancient-woodland&offset=50&limit=100
```

Request for issues for a specific resource:

```
curl http://localhost:8000/log/issue?resource=4a57239e3c1174c80b6d4a0278ab386a7c3664f2e985b2e07a66bbec84988b30
```

Request for issues for a specific dataset and resource:

```
curl http://localhost:8000/log/issue?dataset=border&resource=4a57239e3c1174c80b6d4a0278ab386a7c3664f2e985b2e07a66bbec84988b30&field=geometry
```

### /performance/provision_summary

S3 path: `data/performance/provision_summary.parquet`

```
http://localhost:8000/performance/provision_summary?organisation=local-authority:LBH&offset=50&limit=100
```

Optional Parameters:
 * `offset`
 * `limit`
 * `organisation`
 * `dataset`

### /performance/issue_type_summary

S3 path: `data/performance/endpoint_dataset_issue_type_summary.parquet`

```
http://localhost:8000/performance/issue_type_summary?dataset=ancient-woodland&severity=error&responsibility=external
```

Optional Parameters:
 * `offset`
 * `limit`
 * `dataset`
 * `organisation`
 * `issueType`
 * `issueField`
 * `severity`
 * `responsibility`
 * `resource` (comma-separated list of resource hashes)

### /performance/dataset_resource_mapping

S3 path: `data/performance/endpoint_dataset_resource_summary.parquet`

```
http://localhost:8000/performance/dataset_resource_mapping?dataset=ancient-woodland
```

Optional Parameters:
 * `offset`
 * `limit`
 * `dataset`
 * `organisation`
 * `endpoint_url`

### /performance/endpoint_dataset_summary

S3 path: `data/performance/endpoint_dataset_summary.parquet`

```
http://localhost:8000/performance/endpoint_dataset_summary?dataset=ancient-woodland
```

Optional Parameters:
 * `offset`
 * `limit`
 * `dataset`
 * `organisation`

### /specification/specification

S3 path: `data/specification/*.parquet`

```
http://localhost:8000/specification/specification?offset=0&limit=10
```

Optional Parameters:
 * `offset`
 * `limit`
 * `dataset`
