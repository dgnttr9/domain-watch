from datetime import datetime, timezone

from app.providers.base import ProviderResult, ProviderStatus
from app.providers.registry import ProviderRegistry


class SuccessProvider:
    name = "rdap"

    def lookup(self, domain: str) -> ProviderResult:
        return ProviderResult(
            provider=self.name,
            status=ProviderStatus.ACTIVE,
            expiration_date=datetime(2026, 6, 1, tzinfo=timezone.utc),
        )


def test_list_logs_with_domain_filter(client, monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.v1.routes.domains.build_provider_registry",
        lambda: ProviderRegistry(providers=[SuccessProvider()]),
    )
    check_response = client.post("/api/v1/domains/check", json={"domains": ["openai.com"]})
    domain_id = check_response.json()["data"][0]["id"]

    response = client.get(f"/api/v1/logs?domain_id={domain_id}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    assert payload["data"][0]["domain_id"] == domain_id
