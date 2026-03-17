from __future__ import annotations

from datetime import datetime

import httpx

from app.core.config import get_settings
from app.providers.base import ProviderResult, ProviderStatus
from app.providers.normalizers import truncate_excerpt


class RdapProvider:
    name = "rdap"

    def __init__(self, timeout_seconds: float = 8.0) -> None:
        self.timeout_seconds = timeout_seconds
        self.settings = get_settings()

    def lookup(self, domain: str) -> ProviderResult:
        url = f"https://rdap.org/domain/{domain}"
        try:
            with httpx.Client(timeout=self.timeout_seconds, follow_redirects=True) as client:
                response = client.get(url)
            if response.status_code == 404:
                return ProviderResult(
                    provider=self.name,
                    status=ProviderStatus.AVAILABLE,
                    raw_status="not_found",
                    raw_response_excerpt=truncate_excerpt(
                        response.text,
                        self.settings.raw_response_excerpt_limit,
                    ),
                )

            response.raise_for_status()
            data = response.json()
            expiration_date = self._extract_expiration_date(data)
            return ProviderResult(
                provider=self.name,
                status=ProviderStatus.ACTIVE if expiration_date else ProviderStatus.UNKNOWN,
                expiration_date=expiration_date,
                raw_status="expiration_found" if expiration_date else "expiration_missing",
                raw_response_excerpt=truncate_excerpt(
                    response.text,
                    self.settings.raw_response_excerpt_limit,
                ),
            )
        except httpx.TimeoutException:
            return ProviderResult(
                provider=self.name,
                status=ProviderStatus.ERROR,
                error_code="rdap_timeout",
                error_message="RDAP request timed out.",
            )
        except httpx.HTTPError as exc:
            return ProviderResult(
                provider=self.name,
                status=ProviderStatus.ERROR,
                error_code="rdap_http_error",
                error_message=str(exc),
            )
        except Exception as exc:  # pragma: no cover
            return ProviderResult(
                provider=self.name,
                status=ProviderStatus.ERROR,
                error_code="rdap_unexpected_error",
                error_message=str(exc),
            )

    @staticmethod
    def _extract_expiration_date(payload: dict) -> datetime | None:
        for event in payload.get("events", []):
            if event.get("eventAction") == "expiration" and event.get("eventDate"):
                return datetime.fromisoformat(event["eventDate"].replace("Z", "+00:00"))
        return None
