from pathlib import Path

from app.core.models import PatientRecord
from app.services.patient_data_service import PatientDataService


class PatientAPIService:
    """Application service for API-facing patient operations."""

    def __init__(self, csv_path: Path) -> None:
        self.service = PatientDataService(csv_path)

    def list_patients(self) -> list[PatientRecord]:
        return self.service.list_patients()

    def get_patient(self, patient_id: str) -> PatientRecord | None:
        return self.service.get_patient(patient_id)

    def patient_count(self) -> int:
        return self.service.patient_count()
