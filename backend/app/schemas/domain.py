from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.enums.scheduler import SchedulerPreset


class DomainCreateRequest(BaseModel):
    domain: str
    scheduler_enabled: bool = False
    scheduler_preset: SchedulerPreset | None = None


class DomainCheckRequest(BaseModel):
    domains: list[str] = Field(min_length=1)


class DomainSchedulerUpdateRequest(BaseModel):
    scheduler_enabled: bool
    scheduler_preset: SchedulerPreset | None = None


class DomainResponse(BaseModel):
    id: int
    domain: str
    status: str
    provider_used: str | None
    expiration_date: datetime | None
    days_left: int | None
    last_checked_at: datetime | None
    next_check_at: datetime | None
    scheduler_enabled: bool
    scheduler_preset: str | None
    last_error_message: str | None

    @classmethod
    def from_model(cls, model: object) -> "DomainResponse":
        return cls(
            id=model.id,
            domain=model.domain,
            status=model.status,
            provider_used=model.provider_used,
            expiration_date=model.expiration_date,
            days_left=model.days_left,
            last_checked_at=model.last_checked_at,
            next_check_at=model.next_check_at,
            scheduler_enabled=model.scheduler_enabled,
            scheduler_preset=model.scheduler_preset,
            last_error_message=model.last_error_message,
        )
