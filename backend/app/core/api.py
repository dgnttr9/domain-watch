from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str
    message: str
    field: str | None = None


class ApiResponse(BaseModel):
    status: str
    message: str
    data: Any = None
    errors: list[ErrorDetail] = Field(default_factory=list)


def success_response(message: str, data: Any = None) -> ApiResponse:
    return ApiResponse(status="success", message=message, data=data, errors=[])


def error_response(message: str, errors: list[ErrorDetail], status: str = "error") -> ApiResponse:
    return ApiResponse(status=status, message=message, data=None, errors=errors)
