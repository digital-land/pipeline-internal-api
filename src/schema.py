from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field


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
