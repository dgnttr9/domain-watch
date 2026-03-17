from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import AppLog
from app.repositories.log_repository import LogRepository


class LogService:
    def __init__(self, *, session: Session) -> None:
        self.session = session
        self.log_repository = LogRepository(session)

    def create_log(
        self,
        *,
        level: str,
        scope: str,
        message: str,
        domain_id: int | None = None,
        run_id: int | None = None,
        metadata_json: dict | None = None,
    ) -> AppLog:
        entry = AppLog(
            level=level,
            scope=scope,
            message=message,
            domain_id=domain_id,
            run_id=run_id,
            metadata_json=metadata_json,
        )
        self.log_repository.add(entry)
        return entry

    def list_logs(
        self,
        *,
        level: str | None = None,
        domain_id: int | None = None,
        created_from: datetime | None = None,
        created_to: datetime | None = None,
    ) -> list[AppLog]:
        return self.log_repository.list_logs(
            level=level,
            domain_id=domain_id,
            created_from=created_from,
            created_to=created_to,
        )
