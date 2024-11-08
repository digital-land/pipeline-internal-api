import os

from fastapi import FastAPI

from schema import HealthCheckResponse

app = FastAPI()


@app.get("/health", response_model=HealthCheckResponse)
def healthcheck():
    return HealthCheckResponse(
        name="pipeline-api",
        version=os.environ.get("GIT_COMMIT", "unknown")
    )
