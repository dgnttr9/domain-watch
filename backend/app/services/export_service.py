from __future__ import annotations

import csv
import io
from datetime import datetime

from sqlalchemy.orm import Session

from app.repositories.domain_repository import DomainRepository


class ExportService:
    def __init__(self, *, session: Session) -> None:
        self.session = session
        self.domain_repository = DomainRepository(session)

    def export_domains_json(self) -> list[dict]:
        return [self._serialize_domain(item) for item in self.domain_repository.list_all()]

    def export_domains_csv(self) -> str:
        output = io.StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=[
                "id",
                "domain",
                "status",
                "provider_used",
                "expiration_date",
                "days_left",
                "last_checked_at",
                "next_check_at",
                "scheduler_enabled",
                "scheduler_preset",
                "last_error_message",
            ],
        )
        writer.writeheader()
        for item in self.domain_repository.list_all():
            writer.writerow(self._serialize_domain(item))
        return output.getvalue()

    @staticmethod
    def _serialize_domain(item) -> dict:
        return {
            "id": item.id,
            "domain": item.domain,
            "status": item.status,
            "provider_used": item.provider_used,
            "expiration_date": ExportService._isoformat(item.expiration_date),
            "days_left": item.days_left,
            "last_checked_at": ExportService._isoformat(item.last_checked_at),
            "next_check_at": ExportService._isoformat(item.next_check_at),
            "scheduler_enabled": item.scheduler_enabled,
            "scheduler_preset": item.scheduler_preset,
            "last_error_message": item.last_error_message,
        }

    @staticmethod
    def _isoformat(value: datetime | None) -> str | None:
        return value.isoformat() if value else None
