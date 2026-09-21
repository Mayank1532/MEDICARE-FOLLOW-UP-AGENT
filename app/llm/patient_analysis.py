from typing import cast

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from app.llm.ollama import get_llm


class PatientFollowupAnalysis(BaseModel):
    analysis: str = Field(
        description="Concise care-coordination analysis based only on the supplied patient record."
    )
    recommended_action: str = Field(
        description="Prioritized follow-up action for the care team."
    )


SYSTEM_PROMPT = """
You are a healthcare follow-up decision-support assistant.

Analyze only the patient information supplied in the request.

Your role is care coordination and follow-up prioritization.
Do not diagnose diseases.
Do not prescribe, change, or discontinue medication.
Do not invent missing patient information.
Do not make unsupported clinical claims.

Return:
1. A concise analysis of the follow-up situation.
2. A prioritized follow-up action for the care team.

Base both fields only on the supplied patient record.
""".strip()


def analyze_patient_with_llm(
    patient_data: dict[str, object],
) -> PatientFollowupAnalysis:
    llm = get_llm().with_structured_output(PatientFollowupAnalysis)

    prompt = (
        "Review the following patient record for follow-up prioritization.\n\n"
        f"Patient record:\n{patient_data}"
    )

    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]
    )

    return cast(PatientFollowupAnalysis, response)
