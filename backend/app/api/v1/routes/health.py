from fastapi import APIRouter

from app.core.api import ApiResponse, success_response
from app.core.config import get_settings


router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=ApiResponse)
def get_health() -> ApiResponse:
    settings = get_settings()
    return success_response(
        "Health check completed.",
        {"application": settings.app_name, "status": "ok"},
    )
