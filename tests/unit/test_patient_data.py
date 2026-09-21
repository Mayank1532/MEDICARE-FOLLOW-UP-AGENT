from pathlib import Path

from app.core.models import PatientRecord
from app.core.repository import PatientRepository
from app.services.patient_data_service import PatientDataService

DATA_PATH = Path("data/patient_data.csv")


def test_patient_dataset_exists() -> None:
    assert DATA_PATH.exists()


def test_patient_repository_loads_records() -> None:
    repository = PatientRepository(DATA_PATH)

    patients = repository.load_all()

    assert len(patients) == 100
    assert all(isinstance(patient, PatientRecord) for patient in patients)


def test_patient_ids_are_unique() -> None:
    repository = PatientRepository(DATA_PATH)

    patients = repository.load_all()
    patient_ids = [patient.patient_id for patient in patients]

    assert len(patient_ids) == len(set(patient_ids))


def test_patient_lookup() -> None:
    service = PatientDataService(DATA_PATH)

    patient = service.get_patient("P0001")

    assert patient is not None
    assert patient.patient_id == "P0001"


def test_missing_patient_returns_none() -> None:
    service = PatientDataService(DATA_PATH)

    patient = service.get_patient("P9999")

    assert patient is None


def test_patient_count() -> None:
    service = PatientDataService(DATA_PATH)

    assert service.patient_count() == 100
