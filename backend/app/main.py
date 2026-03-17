from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.routes.domains import router as domains_router
from app.api.v1.routes.exports import router as exports_router
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.imports import router as imports_router
from app.api.v1.routes.logs import router as logs_router
from app.api.v1.routes.scheduler import router as scheduler_router
from app.core.api import ErrorDetail, error_response
from app.core.config import get_settings
from app.core.exceptions import DomainWatchError


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, debug=settings.app_debug)

    @app.exception_handler(DomainWatchError)
    async def handle_domain_watch_error(_, exc: DomainWatchError) -> JSONResponse:
        payload = error_response(
            exc.message,
            [
                ErrorDetail(
                    code=detail.get("code", exc.code),
                    message=detail.get("message", exc.message),
                    field=detail.get("field"),
                )
                for detail in (exc.details or [{"code": exc.code, "message": exc.message}])
            ],
        )
        return JSONResponse(status_code=exc.status_code, content=payload.model_dump())

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation_error(_, exc: RequestValidationError) -> JSONResponse:
        errors = [
            ErrorDetail(
                code="request_validation_error",
                message=error["msg"],
                field=".".join(map(str, error["loc"][1:])),
            )
            for error in exc.errors()
        ]
        payload = error_response("Request validation failed.", errors)
        return JSONResponse(status_code=422, content=payload.model_dump())

    @app.exception_handler(ValueError)
    async def handle_value_error(_, exc: ValueError) -> JSONResponse:
        payload = error_response(
            str(exc),
            [ErrorDetail(code="value_error", message=str(exc))],
        )
        return JSONResponse(status_code=400, content=payload.model_dump())

    app.include_router(health_router, prefix="/api/v1")
    app.include_router(domains_router, prefix="/api/v1")
    app.include_router(exports_router, prefix="/api/v1")
    app.include_router(imports_router, prefix="/api/v1")
    app.include_router(logs_router, prefix="/api/v1")
    app.include_router(scheduler_router, prefix="/api/v1")
    return app


app = create_app()
