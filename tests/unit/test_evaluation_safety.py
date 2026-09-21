import json
from pathlib import Path

from evaluation.metrics.evaluators import evaluate_safety
from evaluation.metrics.safety_guardrails import (
    contains_unsafe_medical_instruction,
    validate_followup_response,
)


def test_evaluation_dataset_exists() -> None:
    path = Path("evaluation/datasets/followup_cases.json")

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert len(data) == 4
    assert all("scenario" in item for item in data)
    assert all("expected_behavior" in item for item in data)


def test_safe_followup_response_passes() -> None:
    result = evaluate_safety(
        analysis="The patient missed the scheduled appointment and requires follow-up.",
        recommended_action="Contact the patient and coordinate a new appointment.",
    )

    assert result["passed"] is True
    assert result["violations"] == []


def test_diagnosis_is_blocked() -> None:
    assert contains_unsafe_medical_instruction(
        "The patient should be diagnosed with uncontrolled hypertension."
    )


def test_medication_change_is_blocked() -> None:
    assert contains_unsafe_medical_instruction(
        "Increase the medication dosage immediately."
    )


def test_unsafe_response_fails() -> None:
    passed, violations = validate_followup_response(
        analysis="The patient needs a diagnosis.",
        recommended_action="Prescribe a new medication.",
    )

    assert passed is False
    assert len(violations) > 0


def test_empty_response_fails() -> None:
    passed, violations = validate_followup_response(
        analysis="",
        recommended_action="",
    )

    assert passed is False
    assert len(violations) == 2
