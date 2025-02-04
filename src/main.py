from fastapi import Response
from fastapi.openapi.models import Contact

import db
import json
from fastapi import FastAPI, Depends, Request
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from schema import HealthCheckResponse, IssuesParams, ProvisionParams
from log import get_logger

from doc import app_info

app = FastAPI(
    title=app_info.title,
    summary=app_info.summary,
    version=app_info.version,
    contact=Contact(email=app_info.contact),
)
logger = get_logger(__name__)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    # Extract the error details
    errors = exc.errors()
    error_messages = []

    # Loop through the errors and build a custom message
    for error in errors:
        loc = ".".join(
            str(x) for x in error["loc"]
        )  # Location of the error (e.g., "query.dataset")
        msg = error["msg"]  # Error message (e.g., "field required")
        error_messages.append(f"{loc}: {msg}")

    return JSONResponse(status_code=400, content={"detail": error_messages})


@app.get("/log/issue", tags=["Issue"])
def issues(http_response: Response, params: IssuesParams = Depends()):
    paginated_result = db.search_issues(params)
    http_response.headers["X-Pagination-Total-Results"] = str(
        paginated_result.total_results_available
    )
    http_response.headers["X-Pagination-Offset"] = str(paginated_result.params.offset)
    http_response.headers["X-Pagination-Limit"] = str(paginated_result.params.limit)
    return Response(
        content=json.dumps(paginated_result.data),
        media_type="application/json",
        headers=http_response.headers,
    )


@app.get("/performance/provision_summary", tags=["provision_summary"])
def provision_summary(http_response: Response, params: ProvisionParams = Depends()):
    paginated_result = db.search_provision_summary(params)
    http_response.headers["X-Pagination-Total-Results"] = str(
        paginated_result.total_results_available
    )
    http_response.headers["X-Pagination-Offset"] = str(paginated_result.params.offset)
    http_response.headers["X-Pagination-Limit"] = str(paginated_result.params.limit)
    return Response(
        content=json.dumps(paginated_result.data),
        media_type="application/json",
        headers=http_response.headers,
    )


@app.get("/specification/specification", tags=["specification"])
def get_specification(http_response: Response, params: ProvisionParams = Depends()):
    paginated_result = db.get_specification(params)
    http_response.headers["X-Pagination-Total-Results"] = str(
        paginated_result.total_results_available
    )
    http_response.headers["X-Pagination-Offset"] = str(paginated_result.params.offset)
    http_response.headers["X-Pagination-Limit"] = str(paginated_result.params.limit)
    return Response(
        content=json.dumps(paginated_result.data),
        media_type="application/json",
        headers=http_response.headers,
    )


@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
def healthcheck():
    return HealthCheckResponse(name="pipeline-api", version=app.version)
