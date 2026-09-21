from __future__ import annotations

from typing import Any

from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase


def build_followup_test_cases() -> list[LLMTestCase]:
    """Build representative follow-up evaluation cases."""
    return [
        LLMTestCase(
            input=(
                "Patient P0018 missed the last appointment. "
                "Recommend an appropriate follow-up action."
            ),
            actual_output=(
                "The patient requires appointment follow-up. "
                "Contact the patient and coordinate a new appointment."
            ),
            expected_output=(
                "The patient should be contacted and the missed "
                "appointment should be rescheduled."
            ),
        )
    ]


def run_deepeval() -> Any:
    """Run the DeepEval answer-relevancy evaluation."""
    metric = AnswerRelevancyMetric(
        threshold=0.5,
        include_reason=True,
    )

    # DeepEval exposes evaluate as a runtime callable while its
    # current type information is interpreted as a module by MyPy.
    result = evaluate(  # type: ignore[operator]
        test_cases=build_followup_test_cases(),
        metrics=[metric],
    )
    return result


if __name__ == "__main__":
    run_deepeval()
