from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.providers.registry import ProviderRegistry
from app.repositories.domain_repository import DomainRepository
from app.services.domain_check_service import DomainCheckService


class SchedulerDispatchService:
    def __init__(
        self,
        *,
        session: Session,
        provider_registry: ProviderRegistry,
    ) -> None:
        self.session = session
        self.provider_registry = provider_registry
        self.domain_repository = DomainRepository(session)

    def dispatch_due_domains(self, limit: int = 25) -> list:
        due_domains = self.domain_repository.list_due_for_scheduler(
            current_time=datetime.now(timezone.utc),
            limit=limit,
        )
        if not due_domains:
            return []

        check_service = DomainCheckService(
            session=self.session,
            provider_registry=self.provider_registry,
        )
        return check_service.check_domains(
            [item.domain for item in due_domains],
            trigger_source="scheduler",
        )
