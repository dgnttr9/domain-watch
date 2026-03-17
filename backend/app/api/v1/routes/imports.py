from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.api import ApiResponse, success_response
from app.db.session import get_db_session
from app.schemas.import_schema import ImportJobResponse, TextImportRequest
from app.services.domain_import_service import DomainImportService


router = APIRouter(prefix="/imports", tags=["imports"])


def _to_response(job) -> ImportJobResponse:
    return ImportJobResponse(
        id=job.id,
        source_type=job.source_type,
        file_name=job.file_name,
        total_rows=job.total_rows,
        valid_rows=job.valid_rows,
        invalid_rows=job.invalid_rows,
        status=job.status,
        error_summary=job.error_summary,
    )


@router.post("/text", response_model=ApiResponse)
def import_text(
    request: TextImportRequest,
    session: Session = Depends(get_db_session),
) -> ApiResponse:
    service = DomainImportService(session=session)
    job = service.import_text(request.content)
    return success_response("Text import completed.", _to_response(job))


@router.post("/file", response_model=ApiResponse)
async def import_file(
    file: UploadFile = File(...),
    session: Session = Depends(get_db_session),
) -> ApiResponse:
    content = await file.read()
    service = DomainImportService(session=session)

    if file.filename and file.filename.lower().endswith(".txt"):
        job = service.import_text(content.decode("utf-8"))
    elif file.filename and file.filename.lower().endswith(".csv"):
        job = service.import_csv(file.filename, content)
    else:
        raise ValueError("Only .txt and .csv files are supported.")

    return success_response("File import completed.", _to_response(job))
