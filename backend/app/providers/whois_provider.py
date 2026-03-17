from __future__ import annotations

import re
import socket
from datetime import datetime, timezone

from app.core.config import get_settings
from app.providers.base import ProviderResult, ProviderStatus
from app.providers.normalizers import truncate_excerpt


WHOIS_PATTERNS = (
    r"Registry Expiry Date:\s*(?P<value>.+)",
    r"Expiration Date:\s*(?P<value>.+)",
    r"paid-till:\s*(?P<value>.+)",
)


class WhoisProvider:
    name = "whois"

    def __init__(self, timeout_seconds: float = 8.0, server: str = "whois.verisign-grs.com") -> None:
        self.timeout_seconds = timeout_seconds
        self.server = server
        self.settings = get_settings()

    def lookup(self, domain: str) -> ProviderResult:
        try:
            raw = self._query(domain)
            expiration_date = self._extract_expiration_date(raw)
            status = ProviderStatus.ACTIVE if expiration_date else ProviderStatus.UNKNOWN
            return ProviderResult(
                provider=self.name,
                status=status,
                expiration_date=expiration_date,
                raw_status="expiration_found" if expiration_date else "expiration_missing",
                raw_response_excerpt=truncate_excerpt(raw, self.settings.raw_response_excerpt_limit),
            )
        except TimeoutError:
            return ProviderResult(
                provider=self.name,
                status=ProviderStatus.ERROR,
                error_code="whois_timeout",
                error_message="WHOIS request timed out.",
            )
        except Exception as exc:  # pragma: no cover
            return ProviderResult(
                provider=self.name,
                status=ProviderStatus.ERROR,
                error_code="whois_error",
                error_message=str(exc),
            )

    def _query(self, domain: str) -> str:
        with socket.create_connection((self.server, 43), timeout=self.timeout_seconds) as sock:
            sock.sendall(f"{domain}\r\n".encode("utf-8"))
            chunks: list[bytes] = []
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                chunks.append(data)
        return b"".join(chunks).decode("utf-8", errors="replace")

    @staticmethod
    def _extract_expiration_date(raw_text: str) -> datetime | None:
        for pattern in WHOIS_PATTERNS:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if not match:
                continue
            value = match.group("value").strip()
            for parser in (
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d",
                "%d-%b-%Y",
            ):
                try:
                    parsed = datetime.strptime(value, parser)
                    return parsed.replace(tzinfo=timezone.utc)
                except ValueError:
                    continue
        return None
