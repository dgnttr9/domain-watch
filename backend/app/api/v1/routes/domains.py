from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.api import ApiResponse, success_response
from app.db.session import get_db_session
from app.providers.registry import build_provider_registry
from app.schemas.domain import DomainCheckRequest, DomainCreateRequest, DomainResponse
from app.services.domain_check_service import DomainCheckService
from app.services.domain_service import DomainService


router = APIRouter(prefix="/domains", tags=["domains"])


@router.get("", response_model=ApiResponse)
def list_domains(session: Session = Depends(get_db_session)) -> ApiResponse:
    service = DomainService(session=session)
    domains = [DomainResponse.from_model(item) for item in service.list_domains()]
    return success_response("Domains retrieved.", domains)


@router.post("", response_model=ApiResponse)
def create_domain(
    request: DomainCreateRequest,
    session: Session = Depends(get_db_session),
) -> ApiResponse:
    service = DomainService(session=session)
    domain = service.create_domain(
        domain=request.domain,
        scheduler_enabled=request.scheduler_enabled,
        scheduler_preset=request.scheduler_preset.value if request.scheduler_preset else None,
    )
    return success_response("Domain created.", DomainResponse.from_model(domain))


@router.post("/check", response_model=ApiResponse)
def check_domains(
    request: DomainCheckRequest,
    session: Session = Depends(get_db_session),
) -> ApiResponse:
    service = DomainCheckService(session=session, provider_registry=build_provider_registry())
    domains = [DomainResponse.from_model(item) for item in service.check_domains(request.domains)]
    return success_response("Domain check completed.", domains)


@router.post("/{domain_id}/recheck", response_model=ApiResponse)
def recheck_domain(domain_id: int, session: Session = Depends(get_db_session)) -> ApiResponse:
    service = DomainCheckService(session=session, provider_registry=build_provider_registry())
    domain = service.recheck_domain(domain_id)
    return success_response("Domain rechecked.", DomainResponse.from_model(domain))
