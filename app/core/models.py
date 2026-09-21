from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class PatientRecord(BaseModel):
    """Validated representation of one MediCare patient record."""

    model_config = ConfigDict(extra="forbid")

    patient_id: str = Field(min_length=1)
    patient_name: str = Field(min_length=1)
    age: int = Field(ge=0)
    gender: str = Field(min_length=1)
    diagnosis: str = Field(min_length=1)
    current_medication: str = Field(min_length=1)
    lab_test: str = Field(min_length=1)
    lab_value: float
    lab_unit: str = Field(min_length=1)
    last_visit_date: date
    next_scheduled_visit: date
    days_since_last_visit: int = Field(ge=0)
    missed_last_appointment: str = Field(min_length=1)
    vitals_bp_systolic: int = Field(ge=0)
    vitals_bp_diastolic: int = Field(ge=0)
    vitals_heart_rate: int = Field(ge=0)
    vitals_spo2: int = Field(ge=0, le=100)
    notes: str = ""
