from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class LogResponse(BaseModel):
    id: int
    level: str
    scope: str
    message: str
    domain_id: int | None
    run_id: int | None
    metadata_json: dict | None
    created_at: datetime

    @classmethod
    def from_model(cls, model: object) -> "LogResponse":
        return cls(
            id=model.id,
            level=model.level,
            scope=model.scope,
            message=model.message,
            domain_id=model.domain_id,
            run_id=model.run_id,
            metadata_json=model.metadata_json,
            created_at=model.created_at,
        )
