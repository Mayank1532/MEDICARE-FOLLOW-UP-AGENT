from pathlib import Path

from app.core.models import PatientRecord
from app.core.repository import PatientRepository


class PatientDataService:
    """Application service for patient data access."""

    def __init__(self, csv_path: Path) -> None:
        self.repository = PatientRepository(csv_path)

    def list_patients(self) -> list[PatientRecord]:
        return self.repository.load_all()

    def get_patient(self, patient_id: str) -> PatientRecord | None:
        return self.repository.get_by_patient_id(patient_id)

    def patient_count(self) -> int:
        return len(self.repository.load_all())
