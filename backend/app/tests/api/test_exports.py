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


def test_export_domains_json(client, monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.v1.routes.domains.build_provider_registry",
        lambda: ProviderRegistry(providers=[SuccessProvider()]),
    )
    client.post("/api/v1/domains/check", json={"domains": ["openai.com"]})

    response = client.get("/api/v1/exports/domains.json")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    assert payload["data"][0]["domain"] == "openai.com"


def test_export_domains_csv(client) -> None:
    client.post("/api/v1/domains", json={"domain": "openai.com"})

    response = client.get("/api/v1/exports/domains.csv")

    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "openai.com" in response.text
