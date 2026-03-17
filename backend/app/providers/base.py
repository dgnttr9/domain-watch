from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Protocol


class ProviderStatus(StrEnum):
    ACTIVE = "active"
    AVAILABLE = "available"
    ERROR = "error"
    UNKNOWN = "unknown"


@dataclass(slots=True)
class ProviderResult:
    provider: str
    status: ProviderStatus
    expiration_date: datetime | None = None
    raw_status: str | None = None
    error_code: str | None = None
    error_message: str | None = None
    raw_response_excerpt: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    @property
    def is_success(self) -> bool:
        return self.status in {ProviderStatus.ACTIVE, ProviderStatus.AVAILABLE}


class DomainProvider(Protocol):
    name: str

    def lookup(self, domain: str) -> ProviderResult:
        """Resolve the domain expiration status."""
