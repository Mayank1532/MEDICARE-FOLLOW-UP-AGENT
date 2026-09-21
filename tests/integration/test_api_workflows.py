from fastapi.testclient import TestClient

from app.llm.patient_analysis import PatientFollowupAnalysis
from app.main import app

client = TestClient(app)


def mock_llm_result(patient: dict[str, object]) -> PatientFollowupAnalysis:
    """Return deterministic structured LLM output for API integration testing."""
    return PatientFollowupAnalysis(
        analysis=(
            f"Follow-up review completed for {patient['patient_name']} "
            "using the supplied patient information."
        ),
        recommended_action=(
            "Prioritize routine care-coordination follow-up "
            "based on the available record."
        ),
    )


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "healthy"
    assert body["service"] == "MediCare Follow-Up Agent"


def test_patient_list_endpoint() -> None:
    response = client.get("/api/v1/patients")

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 100
    assert len(body["patients"]) == 100


def test_existing_patient_endpoint() -> None:
    response = client.get("/api/v1/patients/P0001")

    assert response.status_code == 200

    body = response.json()

    assert body["patient_id"] == "P0001"
    assert body["patient_name"]


def test_missing_patient_endpoint() -> None:
    response = client.get("/api/v1/patients/P9999")

    assert response.status_code == 404


def test_patient_analysis_workflow(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.agent.graph.analyze_patient_with_llm",
        mock_llm_result,
    )

    response = client.post(
        "/api/v1/workflows/patients/P0001/analysis"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["patient_id"] == "P0001"
    assert body["patient_name"]
    assert body["analysis"]
    assert body["recommended_action"]


def test_missed_appointment_workflow(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.agent.graph.analyze_patient_with_llm",
        mock_llm_result,
    )

    response = client.post(
        "/api/v1/workflows/patients/P0018/missed-appointment"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["patient_id"] == "P0018"
    assert body["patient_name"]
    assert body["analysis"]
    assert body["recommended_action"]


def test_non_missed_appointment_workflow() -> None:
    response = client.post(
        "/api/v1/workflows/patients/P0001/missed-appointment"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["patient_id"] == "P0001"
    assert body["patient_name"]
    assert body["analysis"]
    assert body["recommended_action"]
