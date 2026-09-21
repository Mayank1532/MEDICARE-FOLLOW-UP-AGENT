from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.error_handlers import (
    app_error_handler,
    unexpected_error_handler,
    validation_error_handler,
)
from app.api.middleware import request_logging_middleware
from app.api.routes.patients import router as patient_router
from app.api.routes.workflows import router as workflow_router
from app.api.schemas.responses import HealthResponse
from app.core.config import settings
from app.core.exceptions import AppError
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Care-coordination decision support API for patient "
        "follow-up workflows."
    ),
)

app.middleware("http")(request_logging_middleware)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(Exception, unexpected_error_handler)

app.include_router(patient_router)
app.include_router(workflow_router)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Return application health information."""
    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        version=settings.app_version,
    )
