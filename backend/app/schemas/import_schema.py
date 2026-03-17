from __future__ import annotations

from pydantic import BaseModel


class TextImportRequest(BaseModel):
    content: str


class ImportJobResponse(BaseModel):
    id: int
    source_type: str
    file_name: str | None
    total_rows: int
    valid_rows: int
    invalid_rows: int
    status: str
    error_summary: str | None
