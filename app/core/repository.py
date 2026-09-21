from pathlib import Path

import pandas as pd

from app.core.models import PatientRecord


class PatientRepository:
    """Read and validate patient records from the project dataset."""

    REQUIRED_COLUMNS = [
        "patient_id",
        "patient_name",
        "age",
        "gender",
        "diagnosis",
        "current_medication",
        "lab_test",
        "lab_value",
        "lab_unit",
        "last_visit_date",
        "next_scheduled_visit",
        "days_since_last_visit",
        "missed_last_appointment",
        "vitals_bp_systolic",
        "vitals_bp_diastolic",
        "vitals_heart_rate",
        "vitals_spo2",
        "notes",
    ]

    def __init__(self, csv_path: Path) -> None:
        self.csv_path = csv_path

    def load_all(self) -> list[PatientRecord]:
        """Load and validate every patient record."""
        if not self.csv_path.exists():
            raise FileNotFoundError(
                f"Patient dataset not found: {self.csv_path}"
            )

        dataframe = pd.read_csv(self.csv_path)

        missing_columns = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in dataframe.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Patient dataset is missing required columns: {missing_columns}"
            )

        dataframe = dataframe[self.REQUIRED_COLUMNS].copy()

        dataframe["last_visit_date"] = pd.to_datetime(
            dataframe["last_visit_date"], errors="raise"
        ).dt.date

        dataframe["next_scheduled_visit"] = pd.to_datetime(
            dataframe["next_scheduled_visit"], errors="raise"
        ).dt.date

        records = dataframe.to_dict(orient="records")

        return [PatientRecord.model_validate(record) for record in records]

    def get_by_patient_id(self, patient_id: str) -> PatientRecord | None:
        """Return one patient by unique patient identifier."""
        for patient in self.load_all():
            if patient.patient_id == patient_id:
                return patient

        return None
