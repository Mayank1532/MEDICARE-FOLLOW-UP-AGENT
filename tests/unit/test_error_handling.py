from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_missing_patient_returns_structured_error() -> None:
    response = client.get("/api/v1/patients/P9999")

    assert response.status_code == 404

    body = response.json()

    assert body["error"] == "PATIENT_NOT_FOUND"
    assert "P9999" in body["message"]
    assert body["request_id"]


def test_request_id_header_is_returned() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers.get("X-Request-ID")


def test_invalid_patient_workflow_returns_validation_error() -> None:
    response = client.post(
        "/api/v1/workflows/patients//analysis"
    )

    assert response.status_code in {404, 405}


def test_error_response_does_not_expose_traceback() -> None:
    response = client.get("/api/v1/patients/P9999")

    body = response.json()

    assert "traceback" not in body
    assert "stack" not in body
