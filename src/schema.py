from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, validator


class BaseParams(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(50, ge=1, le=100)


class CommonParams(BaseParams):
    dataset: Optional[str] = Field(None)
    organisation: Optional[str] = Field(None)


class IssuesParams(BaseParams):
    dataset: Optional[str] = Field(None)
    resource: Optional[str] = Field(None)
    field: Optional[str] = Field(None)
    issue_type: Optional[str] = Field(None)

    @validator("dataset")
    def check_dataset_required(cls, value):
        if value is None:
            raise ValueError("The 'dataset' query parameter is required.")
        return value


def snake_to_slug(snake: str) -> str:
    return snake.lower().replace("_", "-")


class Issue(BaseModel):
    dataset: str
    resource: str
    line_number: int
    entry_number: int
    field: str
    issue_type: str
    value: str
    message: str


class IssueTypeSummaryParams(BaseParams):
    dataset: Optional[str] = Field(None)
    organisation: Optional[str] = Field(None)
    issueType: Optional[str] = Field(None)
    issueField: Optional[str] = Field(None)
    severity: Optional[str] = Field(None)
    responsibility: Optional[str] = Field(None)
    resource: Optional[str] = Field(None)

    @property
    def resource_list(self) -> Optional[list]:
        if self.resource:
            return [r.strip() for r in self.resource.split(",")]
        return None


class DatasetResourceMappingParams(CommonParams):
    endpoint_url: Optional[str] = Field(None)


class SpecificationsParams(BaseParams):
    dataset: Optional[str] = Field(None)


class HealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    UNHEALTHY = "UNHEALTHY"


class DependencyHealth(BaseModel):
    name: str
    status: HealthStatus


class HealthCheckResponse(BaseModel):
    name: str
    version: str
    dependencies: List[DependencyHealth] = []
