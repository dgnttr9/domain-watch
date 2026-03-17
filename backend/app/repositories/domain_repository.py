from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Domain


class DomainRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_domain(self, domain_name: str) -> Domain | None:
        stmt = select(Domain).where(Domain.domain == domain_name)
        return self.session.scalar(stmt)

    def get_by_id(self, domain_id: int) -> Domain | None:
        stmt = select(Domain).where(Domain.id == domain_id)
        return self.session.scalar(stmt)

    def list_all(self) -> list[Domain]:
        stmt = select(Domain).order_by(Domain.created_at.desc(), Domain.id.desc())
        return list(self.session.scalars(stmt))

    def list_due_for_scheduler(self, current_time: datetime, limit: int = 100) -> list[Domain]:
        stmt = (
            select(Domain)
            .where(Domain.scheduler_enabled.is_(True))
            .where(Domain.next_check_at.is_not(None))
            .where(Domain.next_check_at <= current_time)
            .order_by(Domain.next_check_at.asc(), Domain.id.asc())
            .limit(limit)
        )
        return list(self.session.scalars(stmt))

    def add(self, domain: Domain) -> Domain:
        self.session.add(domain)
        return domain

    def delete(self, domain: Domain) -> None:
        self.session.delete(domain)
