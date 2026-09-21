from typing import TypedDict

from app.agent.service import run_agent
from app.core.models import PatientRecord
from app.services.patient_data_service import PatientDataService


class PatientAnalysisResult(TypedDict):
    patient_id: str
    patient_name: str
    analysis: str
    recommended_action: str


class MissedAppointmentResult(TypedDict):
    patient_id: str
    patient_name: str
    missed_appointment: bool
    days_since_last_visit: int
    analysis: str
    recommended_action: str


class FollowupWorkflowService:
    """Coordinates patient follow-up workflows."""

    def __init__(self, data_service: PatientDataService) -> None:
        self.data_service = data_service

    @staticmethod
    def _patient_data(patient: PatientRecord) -> dict[str, object]:
        return {
            "patient_id": patient.patient_id,
            "patient_name": patient.patient_name,
            "age": patient.age,
            "gender": patient.gender,
            "diagnosis": patient.diagnosis,
            "current_medication": patient.current_medication,
            "lab_test": patient.lab_test,
            "lab_value": patient.lab_value,
            "lab_unit": patient.lab_unit,
            "last_visit_date": patient.last_visit_date.isoformat(),
            "next_scheduled_visit": patient.next_scheduled_visit.isoformat(),
            "days_since_last_visit": patient.days_since_last_visit,
            "missed_last_appointment": patient.missed_last_appointment,
            "vitals_bp_systolic": patient.vitals_bp_systolic,
            "vitals_bp_diastolic": patient.vitals_bp_diastolic,
            "vitals_heart_rate": patient.vitals_heart_rate,
            "vitals_spo2": patient.vitals_spo2,
            "notes": patient.notes,
        }

    def analyze_patient(
        self,
        patient_id: str,
    ) -> PatientAnalysisResult | None:
        patient = self.data_service.get_patient(patient_id)

        if patient is None:
            return None

        result = run_agent(
            patient_id=patient.patient_id,
            patient_data=self._patient_data(patient),
        )

        return {
            "patient_id": patient.patient_id,
            "patient_name": patient.patient_name,
            "analysis": str(result.get("analysis", "")),
            "recommended_action": str(
                result.get("recommended_action", "")
            ),
        }

    def analyze_missed_appointment(
        self,
        patient_id: str,
    ) -> MissedAppointmentResult | None:
        patient = self.data_service.get_patient(patient_id)

        if patient is None:
            return None

        missed = patient.missed_last_appointment.strip().lower() in {
            "yes",
            "true",
            "1",
        }

        if not missed:
            return {
                "patient_id": patient.patient_id,
                "patient_name": patient.patient_name,
                "missed_appointment": False,
                "days_since_last_visit": patient.days_since_last_visit,
                "analysis": "No missed appointment is recorded for this patient.",
                "recommended_action": (
                    "No missed-appointment follow-up is required based on "
                    "the available record."
                ),
            }

        result = run_agent(
            patient_id=patient.patient_id,
            patient_data=self._patient_data(patient),
        )

        return {
            "patient_id": patient.patient_id,
            "patient_name": patient.patient_name,
            "missed_appointment": True,
            "days_since_last_visit": patient.days_since_last_visit,
            "analysis": str(result.get("analysis", "")),
            "recommended_action": str(
                result.get("recommended_action", "")
            ),
        }
