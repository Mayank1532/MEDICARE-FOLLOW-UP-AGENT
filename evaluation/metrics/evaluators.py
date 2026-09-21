from __future__ import annotations

from typing import TypedDict

from evaluation.metrics.safety_guardrails import validate_followup_response


class EvaluationResult(TypedDict):
    passed: bool
    violations: list[str]


def evaluate_safety(analysis: str, recommended_action: str) -> EvaluationResult:
    """Run deterministic healthcare safety validation."""
    passed, violations = validate_followup_response(
        analysis=analysis,
        recommended_action=recommended_action,
    )

    return {
        "passed": passed,
        "violations": violations,
    }
