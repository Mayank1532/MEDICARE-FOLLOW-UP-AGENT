from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.api.schemas.workflows import (
    MissedAppointmentResponse,
    PatientAnalysisResponse,
)
from app.services.followup_workflow_service import FollowupWorkflowService
from app.services.patient_data_service import PatientDataService

router = APIRouter(
    prefix="/api/v1/workflows",
    tags=["workflows"],
)

DATA_PATH = Path("data/patient_data.csv")

workflow_service = FollowupWorkflowService(
    PatientDataService(DATA_PATH)
)


@router.post(
    "/patients/{patient_id}/analysis",
    response_model=PatientAnalysisResponse,
)
def analyze_patient(patient_id: str) -> PatientAnalysisResponse:
    result = workflow_service.analyze_patient(patient_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Patient not found: {patient_id}",
        )

    return PatientAnalysisResponse(
        patient_id=result["patient_id"],
        patient_name=result["patient_name"],
        analysis=result["analysis"],
        recommended_action=result["recommended_action"],
    )


@router.post(
    "/patients/{patient_id}/missed-appointment",
    response_model=MissedAppointmentResponse,
)
def analyze_missed_appointment(
    patient_id: str,
) -> MissedAppointmentResponse:
    result = workflow_service.analyze_missed_appointment(patient_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Patient not found: {patient_id}",
        )

    return MissedAppointmentResponse(
        patient_id=result["patient_id"],
        patient_name=result["patient_name"],
        missed_appointment=result["missed_appointment"],
        days_since_last_visit=result["days_since_last_visit"],
        analysis=result["analysis"],
        recommended_action=result["recommended_action"],
    )
