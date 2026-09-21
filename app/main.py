from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import configure_logging

configure_logging(settings.log_level)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return application health information."""

    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
    }
