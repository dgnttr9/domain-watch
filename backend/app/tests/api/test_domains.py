from datetime import datetime, timezone

from app.providers.base import ProviderResult, ProviderStatus
from app.providers.registry import ProviderRegistry


class SuccessProvider:
    name = "rdap"

    def lookup(self, domain: str) -> ProviderResult:
        return ProviderResult(
            provider=self.name,
            status=ProviderStatus.ACTIVE,
            expiration_date=datetime(2026, 4, 1, tzinfo=timezone.utc),
        )


def test_create_domain(client) -> None:
    response = client.post(
        "/api/v1/domains",
        json={"domain": "openai.com", "scheduler_enabled": True, "scheduler_preset": "daily"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    assert payload["data"]["domain"] == "openai.com"
    assert payload["data"]["scheduler_preset"] == "daily"


def test_list_domains(client) -> None:
    client.post("/api/v1/domains", json={"domain": "openai.com"})
    response = client.get("/api/v1/domains")

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1


def test_create_domain_validation_error(client) -> None:
    response = client.post("/api/v1/domains", json={"domain": "not a domain"})

    assert response.status_code == 422
    payload = response.json()
    assert payload["status"] == "error"
    assert payload["errors"][0]["code"] == "invalid_domain_format"


def test_check_domains_endpoint(client, monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.v1.routes.domains.build_provider_registry",
        lambda: ProviderRegistry(providers=[SuccessProvider()]),
    )
    response = client.post("/api/v1/domains/check", json={"domains": ["openai.com"]})

    assert response.status_code == 200
    payload = response.json()
    assert payload["data"][0]["status"] == "active"
    assert payload["data"][0]["provider_used"] == "rdap"


def test_recheck_domain_endpoint(client, monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.v1.routes.domains.build_provider_registry",
        lambda: ProviderRegistry(providers=[SuccessProvider()]),
    )
    create_response = client.post("/api/v1/domains", json={"domain": "openai.com"})
    domain_id = create_response.json()["data"]["id"]

    response = client.post(f"/api/v1/domains/{domain_id}/recheck")

    assert response.status_code == 200
    assert response.json()["data"]["status"] == "active"
