from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_list_patients_endpoint() -> None:
    response = client.get("/api/v1/patients")

    assert response.status_code == 200

    payload = response.json()

    assert payload["count"] == 100
    assert len(payload["patients"]) == 100


def test_get_patient_endpoint() -> None:
    response = client.get("/api/v1/patients/P0001")

    assert response.status_code == 200
    assert response.json()["patient_id"] == "P0001"


def test_missing_patient_endpoint() -> None:
    response = client.get("/api/v1/patients/P9999")

    assert response.status_code == 404

    body = response.json()

    assert body["error"] == "PATIENT_NOT_FOUND"
    assert "Patient not found" in body["message"] or "was not found" in body["message"]
    assert body["request_id"]
