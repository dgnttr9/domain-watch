from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import AppLog


class LogRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, log_entry: AppLog) -> AppLog:
        self.session.add(log_entry)
        return log_entry

    def list_logs(
        self,
        *,
        level: str | None = None,
        domain_id: int | None = None,
        created_from: datetime | None = None,
        created_to: datetime | None = None,
    ) -> list[AppLog]:
        stmt = select(AppLog).order_by(AppLog.created_at.desc(), AppLog.id.desc())
        if level:
            stmt = stmt.where(AppLog.level == level)
        if domain_id is not None:
            stmt = stmt.where(AppLog.domain_id == domain_id)
        if created_from:
            stmt = stmt.where(AppLog.created_at >= created_from)
        if created_to:
            stmt = stmt.where(AppLog.created_at <= created_to)
        return list(self.session.scalars(stmt))
