import os
from typing import List

import db

from fastapi import FastAPI, Depends

from schema import HealthCheckResponse, IssuesParams, Issue

app = FastAPI()


@app.get("/log/issue")
def issues(params: IssuesParams = Depends()):
    return db.search_issues(params)


@app.get("/health", response_model=HealthCheckResponse)
def healthcheck():
    return HealthCheckResponse(
        name="pipeline-api",
        version=os.environ.get("GIT_COMMIT", "unknown")
    )
