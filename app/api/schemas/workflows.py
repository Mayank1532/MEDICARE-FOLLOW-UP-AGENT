from pydantic import BaseModel


class PatientAnalysisResponse(BaseModel):
    patient_id: str
    patient_name: str
    analysis: str
    recommended_action: str


class MissedAppointmentResponse(BaseModel):
    patient_id: str
    patient_name: str
    missed_appointment: bool
    days_since_last_visit: int
    analysis: str
    recommended_action: str
