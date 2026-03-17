from __future__ import annotations

from dataclasses import dataclass

from app.providers.base import DomainProvider
from app.providers.rdap_provider import RdapProvider
from app.providers.whois_provider import WhoisProvider


@dataclass(slots=True)
class ProviderRegistry:
    providers: list[DomainProvider]

    def ordered(self) -> list[DomainProvider]:
        return self.providers


def build_provider_registry() -> ProviderRegistry:
    return ProviderRegistry(providers=[RdapProvider(), WhoisProvider()])
