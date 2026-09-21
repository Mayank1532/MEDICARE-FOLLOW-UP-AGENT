from fastapi import FastAPI

from app.api.routes.patients import router as patient_router
from app.api.routes.workflows import router as workflow_router
from app.api.schemas.responses import HealthResponse
from app.core.config import settings
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
