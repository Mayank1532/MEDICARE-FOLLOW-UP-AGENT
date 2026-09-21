from __future__ import annotations

import re

FORBIDDEN_PATTERNS = (
    r"\bdiagnos(?:e|is|ed|ing)\b",
    r"\bprescrib(?:e|ing|ed|es)\b",
    r"\bchange (?:the )?(?:medication|dose|dosage)\b",
    r"\bstop (?:the )?(?:medication|medicine)\b",
    r"\bincrease (?:the )?(?:medication|dose|dosage)\b",
    r"\bdecrease (?:the )?(?:medication|dose|dosage)\b",
)


def contains_unsafe_medical_instruction(text: str) -> bool:
    """Detect restricted medical instructions in generated text."""
    normalized = text.lower()

    return any(
        re.search(pattern, normalized) is not None
        for pattern in FORBIDDEN_PATTERNS
    )


def validate_followup_response(
    analysis: str,
    recommended_action: str,
) -> tuple[bool, list[str]]:
    """Validate a generated response against safety constraints."""
    violations: list[str] = []

    if contains_unsafe_medical_instruction(
        f"{analysis}\n{recommended_action}"
    ):
        violations.append(
            "Response contains restricted medical instructions."
        )

    if not analysis.strip():
        violations.append("Analysis must not be empty.")

    if not recommended_action.strip():
        violations.append("Recommended action must not be empty.")

    return len(violations) == 0, violations
