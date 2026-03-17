from datetime import datetime, timezone

from app.db.models import Domain
from app.providers.base import ProviderResult, ProviderStatus
from app.providers.registry import ProviderRegistry
from app.services.scheduler_dispatch_service import SchedulerDispatchService


class SuccessProvider:
    name = "rdap"

    def lookup(self, domain: str) -> ProviderResult:
        return ProviderResult(
            provider=self.name,
            status=ProviderStatus.ACTIVE,
            expiration_date=datetime(2026, 8, 1, tzinfo=timezone.utc),
        )


def test_dispatch_due_domains_checks_only_due_items(sqlite_session) -> None:
    sqlite_session.add(
        Domain(
            domain="openai.com",
            status="pending",
            scheduler_enabled=True,
            scheduler_preset="daily",
            next_check_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )
    )
    sqlite_session.commit()

    service = SchedulerDispatchService(
        session=sqlite_session,
        provider_registry=ProviderRegistry(providers=[SuccessProvider()]),
    )

    results = service.dispatch_due_domains(limit=10)

    assert len(results) == 1
    assert results[0].status == "active"
