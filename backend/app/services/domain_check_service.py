from __future__ import annotations

import time
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, ValidationError
from app.core.validation import is_valid_domain, normalize_domain
from app.db.models import Domain, DomainCheckRun
from app.domain.enums.scheduler import SchedulerPreset, SchedulerType
from app.providers.base import ProviderResult, ProviderStatus
from app.providers.registry import ProviderRegistry
from app.repositories.check_run_repository import DomainCheckRunRepository
from app.repositories.domain_repository import DomainRepository
from app.scheduler.presets import compute_next_check_at
from app.services.domain_metrics_service import compute_days_left
from app.services.log_service import LogService


class DomainCheckService:
    def __init__(
        self,
        *,
        session: Session,
        provider_registry: ProviderRegistry,
        max_attempts_per_provider: int = 2,
    ) -> None:
        self.session = session
        self.provider_registry = provider_registry
        self.max_attempts_per_provider = max_attempts_per_provider
        self.domain_repository = DomainRepository(session)
        self.check_run_repository = DomainCheckRunRepository(session)
        self.log_service = LogService(session=session)

    def check_domains(self, domains: list[str], *, trigger_source: str = "manual") -> list[Domain]:
        checked_domains: list[Domain] = []
        try:
            for raw_domain in domains:
                normalized = normalize_domain(raw_domain)
                if not is_valid_domain(normalized):
                    raise ValidationError(
                        f"Invalid domain format: {raw_domain}",
                        code="invalid_domain_format",
                    )

                domain_model = self.domain_repository.get_by_domain(normalized)
                if domain_model is None:
                    domain_model = Domain(domain=normalized, status="pending")
                    self.domain_repository.add(domain_model)
                    self.session.flush()

                result, attempts, attempt_details = self._resolve_with_fallback(normalized)
                self._apply_result(domain_model, result)
                run = self._record_check_run(
                    domain_model,
                    result,
                    trigger_source,
                    attempts,
                    attempt_details,
                )
                self._log_result(domain_model, run.id, result, trigger_source, attempt_details)
                checked_domains.append(domain_model)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

        return checked_domains

    def recheck_domain(self, domain_id: int) -> Domain:
        domain_model = self.domain_repository.get_by_id(domain_id)
        if domain_model is None:
            raise NotFoundError("Domain not found.", code="domain_not_found")
        checked = self.check_domains([domain_model.domain], trigger_source="manual")
        return checked[0]

    def _resolve_with_fallback(self, domain: str) -> tuple[ProviderResult, list[str], list[dict]]:
        attempts: list[str] = []
        attempt_details: list[dict] = []
        result = ProviderResult(provider="unknown", status=ProviderStatus.ERROR, error_code="provider_unavailable")
        for provider in self.provider_registry.ordered():
            for _ in range(self.max_attempts_per_provider):
                attempts.append(provider.name)
                result = provider.lookup(domain)
                attempt_details.append(
                    {
                        "provider": provider.name,
                        "status": result.status,
                        "error_code": result.error_code,
                        "error_message": result.error_message,
                    }
                )
                if result.is_success:
                    return result, attempts, attempt_details
                if result.status == ProviderStatus.UNKNOWN:
                    break
            if result.status == ProviderStatus.UNKNOWN:
                continue
        return result, attempts, attempt_details

    def _apply_result(self, domain_model: Domain, result: ProviderResult) -> None:
        now = datetime.now(timezone.utc)
        domain_model.provider_used = result.provider
        domain_model.last_checked_at = now
        domain_model.expiration_date = result.expiration_date
        domain_model.days_left = compute_days_left(result.expiration_date, now)
        domain_model.last_error_code = result.error_code
        domain_model.last_error_message = result.error_message

        if result.status == ProviderStatus.ACTIVE:
            domain_model.status = "active"
        elif result.status == ProviderStatus.AVAILABLE:
            domain_model.status = "available"
        elif result.status == ProviderStatus.UNKNOWN:
            domain_model.status = "unknown"
        else:
            domain_model.status = "error"

        if domain_model.scheduler_enabled and domain_model.scheduler_preset:
            preset = SchedulerPreset(domain_model.scheduler_preset)
            domain_model.scheduler_type = SchedulerType.PRESET
            domain_model.next_check_at = compute_next_check_at(preset, now)
        else:
            domain_model.next_check_at = None

    def _record_check_run(
        self,
        domain_model: Domain,
        result: ProviderResult,
        trigger_source: str,
        attempts: list[str],
        attempt_details: list[dict],
    ) -> DomainCheckRun:
        run = DomainCheckRun(
            domain_id=domain_model.id,
            requested_by="system",
            trigger_source=trigger_source,
            provider_attempt_order=attempts,
            provider_attempt_details=attempt_details,
            final_provider=result.provider,
            status=domain_model.status,
            expiration_date=domain_model.expiration_date,
            days_left=domain_model.days_left,
            checked_at=domain_model.last_checked_at,
            duration_ms=int(time.time() * 1000) % 1000,
            error_message=result.error_message,
            error_code=result.error_code,
            raw_response_excerpt=result.raw_response_excerpt,
        )
        self.check_run_repository.add(run)
        self.session.flush()
        return run

    def _log_result(
        self,
        domain_model: Domain,
        run_id: int,
        result: ProviderResult,
        trigger_source: str,
        attempt_details: list[dict],
    ) -> None:
        level = "INFO"
        if result.status == ProviderStatus.UNKNOWN:
            level = "WARNING"
        elif result.status == ProviderStatus.ERROR:
            level = "ERROR"

        self.log_service.create_log(
            level=level,
            scope="domain_check",
            message=f"Domain check completed for {domain_model.domain}.",
            domain_id=domain_model.id,
            run_id=run_id,
            metadata_json={
                "trigger_source": trigger_source,
                "final_provider": result.provider,
                "provider_attempts": attempt_details,
                "error_code": result.error_code,
                "error_message": result.error_message,
            },
        )
