from pydantic import BaseModel


class PatientResponse(BaseModel):
    patient_id: str
    patient_name: str
    age: int
    gender: str
    diagnosis: str
    current_medication: str
    lab_test: str
    lab_value: float
    lab_unit: str
    last_visit_date: str
    next_scheduled_visit: str
    days_since_last_visit: int
    missed_last_appointment: str
    vitals_bp_systolic: int
    vitals_bp_diastolic: int
    vitals_heart_rate: int
    vitals_spo2: int
    notes: str


class PatientListResponse(BaseModel):
    count: int
    patients: list[PatientResponse]


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
