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


## Swagger UI

The Swagger UI bundled with Fast API is a useful way to explore the API and try out the endpoints.  It's exposed on the /docs path, e.g.

http://localhost:8000/docs


### Issue endpoint

The /log/issue path exposes issue logs in a paginated result style.  Offset and limit query parameters control the page of results you want to obtain while the X-Pagination-* headers provide the context for where you are within the result set as well as the total results available.

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

### provision_summary endpoint

can be accessed via
```
http://localhost:8000/performance/provision_summary?organisation=local-authority:LBH&offset=50&limit=100
```

Optional Parameters:
 * Offset
 * Limit
 * Organisation
 * Dataset


### specification endpoint

can be accessed via
```
http://localhost:8000/specification/specification?offset=0&limit=10
```

Optional Parameters:
 * Offset
 * Limit
 * Dataset