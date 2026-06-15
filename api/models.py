from pydantic import BaseModel
from typing import Any, Optional


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class RunCaseResponse(BaseModel):
    status: str
    message: str
    outputs: Optional[Any] = None


class FileResponse(BaseModel):
    status: str
    data: Any