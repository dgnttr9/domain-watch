from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, ValidationError
from app.domain.enums.scheduler import SchedulerPreset, SchedulerType
from app.repositories.domain_repository import DomainRepository
from app.repositories.scheduler_repository import SchedulerRepository
from app.scheduler.presets import compute_next_check_at


class SchedulerService:
    def __init__(self, *, session: Session) -> None:
        self.session = session
        self.domain_repository = DomainRepository(session)
        self.scheduler_repository = SchedulerRepository(session)

    def update_domain_schedule(
        self,
        *,
        domain_id: int,
        scheduler_enabled: bool,
        scheduler_preset: str | None,
    ):
        domain = self.domain_repository.get_by_id(domain_id)
        if domain is None:
            raise NotFoundError("Domain not found.", code="domain_not_found")

        if scheduler_enabled and not scheduler_preset:
            raise ValidationError("Scheduler preset is required.", code="scheduler_preset_required")

        try:
            domain.scheduler_enabled = scheduler_enabled
            domain.scheduler_type = SchedulerType.PRESET
            domain.scheduler_preset = scheduler_preset
            domain.scheduler_expression = None
            if scheduler_enabled and scheduler_preset:
                domain.next_check_at = compute_next_check_at(
                    SchedulerPreset(scheduler_preset),
                    datetime.now(timezone.utc),
                )
            else:
                domain.next_check_at = None
            self.scheduler_repository.save(domain)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return domain
