from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_snake, to_camel


class IssuesParams(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(50, ge=1, le=100)
    field: Optional[str] = Field(None)
    issue_type: Optional[str] = Field(None)


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

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            #alias=to_camel
            validation_alias=snake_to_slug,
        )
    )


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
