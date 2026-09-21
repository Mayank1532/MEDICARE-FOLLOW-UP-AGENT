from fastapi import FastAPI

from app.api.middleware import request_logging_middleware
from app.api.routes import patients, workflows
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-style healthcare follow-up decision-support service.",
)

app.middleware("http")(request_logging_middleware)

app.include_router(patients.router)
app.include_router(workflows.router)


@app.get("/health")
def health() -> dict[str, str]:
    """Return application health status."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
    }
