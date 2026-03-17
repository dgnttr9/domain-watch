from enum import StrEnum


class DomainStatus(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    AVAILABLE = "available"
    ERROR = "error"
    UNKNOWN = "unknown"
