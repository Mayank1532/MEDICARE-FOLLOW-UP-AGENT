from fastapi import FastAPI

from app.api.routes.patients import router as patient_router
from app.core.config import settings

app = FastAPI(
    title="MediCare Follow-Up Agent",
    description="Healthcare patient follow-up decision-support API.",
    version=settings.app_version,
)

app.include_router(patient_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
    }
