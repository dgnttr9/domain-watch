from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, ValidationError
from app.core.validation import is_valid_domain, normalize_domain
from app.db.models import Domain
from app.domain.enums.scheduler import SchedulerType
from app.repositories.domain_repository import DomainRepository


class DomainService:
    def __init__(self, *, session: Session) -> None:
        self.session = session
        self.domain_repository = DomainRepository(session)

    def create_domain(
        self,
        *,
        domain: str,
        scheduler_enabled: bool,
        scheduler_preset: str | None,
    ) -> Domain:
        normalized = normalize_domain(domain)
        if not is_valid_domain(normalized):
            raise ValidationError("Invalid domain format.", code="invalid_domain_format")

        existing = self.domain_repository.get_by_domain(normalized)
        if existing:
            raise ValidationError("Domain already exists.", code="domain_already_exists")

        if scheduler_enabled and not scheduler_preset:
            raise ValidationError("Scheduler preset is required.", code="scheduler_preset_required")

        model = Domain(
            domain=normalized,
            status="pending",
            scheduler_enabled=scheduler_enabled,
            scheduler_type=SchedulerType.PRESET,
            scheduler_preset=scheduler_preset,
        )
        try:
            self.domain_repository.add(model)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return model

    def list_domains(self) -> list[Domain]:
        return self.domain_repository.list_all()

    def get_domain(self, domain_id: int) -> Domain:
        model = self.domain_repository.get_by_id(domain_id)
        if model is None:
            raise NotFoundError("Domain not found.", code="domain_not_found")
        return model
