from fastapi import Response
from fastapi.openapi.models import Contact

import db

from fastapi import FastAPI, Depends

from schema import HealthCheckResponse, IssuesParams

from doc import app_info

app = FastAPI(
    title=app_info.title,
    summary=app_info.summary,
    version=app_info.version,
    contact=Contact(email=app_info.contact)
)


@app.get("/log/issue", tags=["Issue"])
def issues(http_response: Response, params: IssuesParams = Depends()):
    paginated_result = db.search_issues(params)
    http_response.headers["X-Pagination-Total-Results"] = str(
        paginated_result.total_results_available
    )
    http_response.headers["X-Pagination-Offset"] = str(paginated_result.params.offset)
    http_response.headers["X-Pagination-Limit"] = str(paginated_result.params.limit)
    return paginated_result.data


@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
def healthcheck():
    return HealthCheckResponse(
        name="pipeline-api",
        version=app.version
    )
