from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.api import ApiResponse, success_response
from app.db.session import get_db_session
from app.providers.registry import build_provider_registry
from app.schemas.domain import DomainResponse, DomainSchedulerUpdateRequest
from app.services.scheduler_dispatch_service import SchedulerDispatchService
from app.services.scheduler_service import SchedulerService


router = APIRouter(prefix="/scheduler", tags=["scheduler"])


@router.put("/domains/{domain_id}", response_model=ApiResponse)
def update_domain_schedule(
    domain_id: int,
    request: DomainSchedulerUpdateRequest,
    session: Session = Depends(get_db_session),
) -> ApiResponse:
    service = SchedulerService(session=session)
    domain = service.update_domain_schedule(
        domain_id=domain_id,
        scheduler_enabled=request.scheduler_enabled,
        scheduler_preset=request.scheduler_preset.value if request.scheduler_preset else None,
    )
    return success_response("Scheduler updated.", DomainResponse.from_model(domain))


@router.post("/dispatch", response_model=ApiResponse)
def dispatch_due_domains(
    limit: int = 25,
    session: Session = Depends(get_db_session),
) -> ApiResponse:
    service = SchedulerDispatchService(
        session=session,
        provider_registry=build_provider_registry(),
    )
    domains = service.dispatch_due_domains(limit=limit)
    return success_response(
        "Scheduler dispatch completed.",
        [DomainResponse.from_model(item) for item in domains],
    )
