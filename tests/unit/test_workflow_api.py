from pathlib import Path
from unittest.mock import patch

import pandas as pd
from fastapi.testclient import TestClient

from app.main import app

DATA_PATH = Path("data/patient_data.csv")

client = TestClient(app)


def get_missed_patient_id() -> str:
    dataframe = pd.read_csv(DATA_PATH)
    values = dataframe["missed_last_appointment"].astype(str).str.strip().str.lower()
    rows = dataframe[values.isin(["yes", "true", "1"])]

    assert not rows.empty

    return str(rows.iloc[0]["patient_id"])


def test_patient_analysis_endpoint() -> None:
    with patch(
        "app.services.followup_workflow_service.run_agent",
        return_value={
            "analysis": "Follow-up review required.",
            "recommended_action": "Contact patient for follow-up.",
        },
    ):
        response = client.post(
            "/api/v1/workflows/patients/P0001/analysis"
        )

    assert response.status_code == 200

    body = response.json()

    assert body["patient_id"] == "P0001"
    assert body["patient_name"] == "Aarav Sharma"
    assert body["analysis"] == "Follow-up review required."
    assert body["recommended_action"] == (
        "Contact patient for follow-up."
    )


def test_missed_appointment_endpoint() -> None:
    patient_id = get_missed_patient_id()

    with patch(
        "app.services.followup_workflow_service.run_agent",
        return_value={
            "analysis": "Missed appointment requires follow-up.",
            "recommended_action": "Contact patient to reschedule.",
        },
    ):
        response = client.post(
            f"/api/v1/workflows/patients/{patient_id}/missed-appointment"
        )

    assert response.status_code == 200

    body = response.json()

    assert body["patient_id"] == patient_id
    assert body["missed_appointment"] is True
    assert body["analysis"] == (
        "Missed appointment requires follow-up."
    )


def test_workflow_endpoint_missing_patient() -> None:
    response = client.post(
        "/api/v1/workflows/patients/P9999/analysis"
    )

    assert response.status_code == 404
    assert "Patient not found" in response.json()["detail"]
