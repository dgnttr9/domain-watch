from __future__ import annotations


class DomainWatchError(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str,
        *,
        code: str = "domain_watch_error",
        status_code: int = 400,
        details: list[dict[str, str]] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or []


class ValidationError(DomainWatchError):
    """Raised when input validation fails."""

    def __init__(self, message: str, *, code: str = "validation_error") -> None:
        super().__init__(message, code=code, status_code=422)


class NotFoundError(DomainWatchError):
    """Raised when an entity is not found."""

    def __init__(self, message: str, *, code: str = "not_found") -> None:
        super().__init__(message, code=code, status_code=404)
