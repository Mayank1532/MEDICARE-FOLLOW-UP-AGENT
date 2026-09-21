from pathlib import Path
from unittest.mock import patch

import pandas as pd

from app.services.followup_workflow_service import FollowupWorkflowService
from app.services.patient_data_service import PatientDataService

DATA_PATH = Path("data/patient_data.csv")


def get_missed_patient_id() -> str:
    dataframe = pd.read_csv(DATA_PATH)
    values = dataframe["missed_last_appointment"].astype(str).str.strip().str.lower()
    rows = dataframe[values.isin(["yes", "true", "1"])]

    assert not rows.empty

    return str(rows.iloc[0]["patient_id"])


def get_non_missed_patient_id() -> str:
    dataframe = pd.read_csv(DATA_PATH)
    values = dataframe["missed_last_appointment"].astype(str).str.strip().str.lower()
    rows = dataframe[~values.isin(["yes", "true", "1"])]

    assert not rows.empty

    return str(rows.iloc[0]["patient_id"])


def test_single_patient_analysis() -> None:
    service = FollowupWorkflowService(
        PatientDataService(DATA_PATH)
    )

    with patch(
        "app.services.followup_workflow_service.run_agent",
        return_value={
            "analysis": "Patient requires routine follow-up review.",
            "recommended_action": "Contact the patient for follow-up.",
        },
    ):
        result = service.analyze_patient("P0001")

    assert result is not None
    assert result["patient_id"] == "P0001"
    assert result["patient_name"] == "Aarav Sharma"
    assert result["analysis"] == (
        "Patient requires routine follow-up review."
    )
    assert result["recommended_action"] == (
        "Contact the patient for follow-up."
    )


def test_single_patient_analysis_missing_patient() -> None:
    service = FollowupWorkflowService(
        PatientDataService(DATA_PATH)
    )

    result = service.analyze_patient("P9999")

    assert result is None


def test_missed_appointment_workflow_for_missed_patient() -> None:
    service = FollowupWorkflowService(
        PatientDataService(DATA_PATH)
    )

    patient_id = get_missed_patient_id()

    with patch(
        "app.services.followup_workflow_service.run_agent",
        return_value={
            "analysis": "Missed appointment requires follow-up.",
            "recommended_action": "Contact patient and review rescheduling.",
        },
    ):
        result = service.analyze_missed_appointment(patient_id)

    assert result is not None
    assert result["patient_id"] == patient_id
    assert result["missed_appointment"] is True
    assert result["analysis"] == (
        "Missed appointment requires follow-up."
    )
    assert result["recommended_action"] == (
        "Contact patient and review rescheduling."
    )


def test_missed_appointment_workflow_for_non_missed_patient() -> None:
    service = FollowupWorkflowService(
        PatientDataService(DATA_PATH)
    )

    patient_id = get_non_missed_patient_id()
    result = service.analyze_missed_appointment(patient_id)

    assert result is not None
    assert result["patient_id"] == patient_id
    assert result["missed_appointment"] is False
    assert "No missed appointment" in str(result["analysis"])
    assert "No missed-appointment follow-up" in str(
        result["recommended_action"]
    )


def test_missed_appointment_missing_patient() -> None:
    service = FollowupWorkflowService(
        PatientDataService(DATA_PATH)
    )

    result = service.analyze_missed_appointment("P9999")

    assert result is None
