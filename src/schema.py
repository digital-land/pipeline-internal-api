from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, validator


class IssuesParams(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(50, ge=1, le=100)
    dataset:  Optional[str] = Field(None)
    resource: Optional[str] = Field(None)
    field: Optional[str] = Field(None)
    issue_type: Optional[str] = Field(None)

    @validator('dataset')
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
