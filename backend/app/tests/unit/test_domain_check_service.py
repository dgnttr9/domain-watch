from datetime import datetime, timezone

from app.providers.base import ProviderResult, ProviderStatus
from app.providers.registry import ProviderRegistry
from app.services.domain_check_service import DomainCheckService


class SuccessProvider:
    name = "rdap"

    def lookup(self, domain: str) -> ProviderResult:
        return ProviderResult(
            provider=self.name,
            status=ProviderStatus.ACTIVE,
            expiration_date=datetime(2026, 4, 1, tzinfo=timezone.utc),
        )


class UnknownProvider:
    name = "rdap"

    def lookup(self, domain: str) -> ProviderResult:
        return ProviderResult(provider=self.name, status=ProviderStatus.UNKNOWN)


class FallbackProvider:
    name = "whois"

    def lookup(self, domain: str) -> ProviderResult:
        return ProviderResult(
            provider=self.name,
            status=ProviderStatus.ACTIVE,
            expiration_date=datetime(2026, 5, 1, tzinfo=timezone.utc),
        )


def test_domain_check_service_creates_and_updates_domain(sqlite_session) -> None:
    service = DomainCheckService(
        session=sqlite_session,
        provider_registry=ProviderRegistry(providers=[SuccessProvider()]),
    )

    result = service.check_domains(["openai.com"])

    assert len(result) == 1
    assert result[0].status == "active"
    assert result[0].provider_used == "rdap"


def test_domain_check_service_uses_fallback_provider(sqlite_session) -> None:
    service = DomainCheckService(
        session=sqlite_session,
        provider_registry=ProviderRegistry(providers=[UnknownProvider(), FallbackProvider()]),
    )

    result = service.check_domains(["example.org"])

    assert result[0].provider_used == "whois"
    assert result[0].status == "active"
