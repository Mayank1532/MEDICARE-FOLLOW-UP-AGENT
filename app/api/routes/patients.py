from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.api.schemas.responses import PatientListResponse, PatientResponse
from app.core.models import PatientRecord
from app.services.patient_api_service import PatientAPIService

router = APIRouter(prefix="/api/v1/patients", tags=["patients"])

DATA_PATH = Path("data/patient_data.csv")
patient_service = PatientAPIService(DATA_PATH)


def to_response(patient: PatientRecord) -> PatientResponse:
    return PatientResponse(
        patient_id=patient.patient_id,
        patient_name=patient.patient_name,
        age=patient.age,
        gender=patient.gender,
        diagnosis=patient.diagnosis,
        current_medication=patient.current_medication,
        lab_test=patient.lab_test,
        lab_value=patient.lab_value,
        lab_unit=patient.lab_unit,
        last_visit_date=patient.last_visit_date.isoformat(),
        next_scheduled_visit=patient.next_scheduled_visit.isoformat(),
        days_since_last_visit=patient.days_since_last_visit,
        missed_last_appointment=patient.missed_last_appointment,
        vitals_bp_systolic=patient.vitals_bp_systolic,
        vitals_bp_diastolic=patient.vitals_bp_diastolic,
        vitals_heart_rate=patient.vitals_heart_rate,
        vitals_spo2=patient.vitals_spo2,
        notes=patient.notes,
    )


@router.get("", response_model=PatientListResponse)
def list_patients() -> PatientListResponse:
    patients = patient_service.list_patients()

    return PatientListResponse(
        count=len(patients),
        patients=[to_response(patient) for patient in patients],
    )


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: str) -> PatientResponse:
    patient = patient_service.get_patient(patient_id)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail=f"Patient not found: {patient_id}",
        )

    return to_response(patient)
