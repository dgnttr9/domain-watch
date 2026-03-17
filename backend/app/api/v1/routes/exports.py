from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.services.export_service import ExportService


router = APIRouter(prefix="/exports", tags=["exports"])


@router.get("/domains.json")
def export_domains_json(session: Session = Depends(get_db_session)) -> JSONResponse:
    service = ExportService(session=session)
    payload = {
        "status": "success",
        "message": "JSON export generated.",
        "data": service.export_domains_json(),
        "errors": [],
    }
    return JSONResponse(content=payload)


@router.get("/domains.csv")
def export_domains_csv(session: Session = Depends(get_db_session)) -> StreamingResponse:
    service = ExportService(session=session)
    content = service.export_domains_csv()
    return StreamingResponse(
        iter([content]),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="domains.csv"'},
    )
