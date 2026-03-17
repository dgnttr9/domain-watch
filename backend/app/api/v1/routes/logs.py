from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.api import ApiResponse, success_response
from app.db.session import get_db_session
from app.schemas.log import LogResponse
from app.services.log_service import LogService


router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("", response_model=ApiResponse)
def list_logs(
    level: str | None = Query(default=None),
    domain_id: int | None = Query(default=None),
    created_from: datetime | None = Query(default=None),
    created_to: datetime | None = Query(default=None),
    session: Session = Depends(get_db_session),
) -> ApiResponse:
    service = LogService(session=session)
    items = service.list_logs(
        level=level,
        domain_id=domain_id,
        created_from=created_from,
        created_to=created_to,
    )
    return success_response("Logs retrieved.", [LogResponse.from_model(item) for item in items])
