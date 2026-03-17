from datetime import datetime, timezone

from app.db.models import Domain
from app.providers.base import ProviderResult, ProviderStatus
from app.providers.registry import ProviderRegistry


class SuccessProvider:
    name = "rdap"

    def lookup(self, domain: str) -> ProviderResult:
        return ProviderResult(
            provider=self.name,
            status=ProviderStatus.ACTIVE,
            expiration_date=datetime(2026, 7, 1, tzinfo=timezone.utc),
        )


def test_update_scheduler(client) -> None:
    create_response = client.post("/api/v1/domains", json={"domain": "openai.com"})
    domain_id = create_response.json()["data"]["id"]

    response = client.put(
        f"/api/v1/scheduler/domains/{domain_id}",
        json={"scheduler_enabled": True, "scheduler_preset": "weekly"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["scheduler_enabled"] is True
    assert payload["data"]["scheduler_preset"] == "weekly"


def test_dispatch_due_domains(client, db_session, monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.v1.routes.scheduler.build_provider_registry",
        lambda: ProviderRegistry(providers=[SuccessProvider()]),
    )
    create_response = client.post(
        "/api/v1/domains",
        json={"domain": "openai.com", "scheduler_enabled": True, "scheduler_preset": "daily"},
    )
    domain_id = create_response.json()["data"]["id"]
    domain = db_session.get(Domain, domain_id)
    domain.next_check_at = datetime(2026, 1, 1, tzinfo=timezone.utc)
    db_session.commit()

    response = client.post("/api/v1/scheduler/dispatch")

    assert response.status_code == 200
    assert response.json()["data"][0]["status"] == "active"
