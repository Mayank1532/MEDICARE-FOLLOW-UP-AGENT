from typing import cast

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from app.llm.ollama import get_llm
from app.mcp.knowledge_tools import search_followup_knowledge


class PatientFollowupAnalysis(BaseModel):
    analysis: str = Field(
        description=(
            "Concise care-coordination analysis based only on the supplied "
            "patient record and retrieved guidance."
        )
    )
    recommended_action: str = Field(
        description="Prioritized follow-up action for the care team."
    )


SYSTEM_PROMPT = """
You are a healthcare follow-up decision-support assistant.

Analyze only the supplied patient record and retrieved follow-up guidance.

Your role is care coordination and follow-up prioritization.
Do not diagnose diseases.
Do not prescribe, change, or discontinue medication.
Do not invent missing patient information.
Do not make unsupported clinical claims.

Use retrieved guidance as supporting knowledge.
If the retrieved guidance does not support a conclusion, do not invent one.

Return:
1. A concise analysis of the follow-up situation.
2. A prioritized follow-up action for the care team.

The recommendation must remain a care-coordination recommendation for human review.
""".strip()


def analyze_patient_with_llm(
    patient_data: dict[str, object],
) -> PatientFollowupAnalysis:
    knowledge_query = (
        "patient follow-up care coordination "
        f"diagnosis={patient_data.get('diagnosis', '')} "
        f"missed appointment={patient_data.get('missed_last_appointment', '')}"
    )

    retrieved_documents = search_followup_knowledge(
        knowledge_query,
        k=3,
    )

    knowledge_context = "\n\n".join(
        str(item["content"])
        for item in retrieved_documents
    )

    llm = get_llm().with_structured_output(PatientFollowupAnalysis)

    prompt = (
        "Review the following patient record.\n\n"
        f"Patient record:\n{patient_data}\n\n"
        "Retrieved follow-up guidance:\n"
        f"{knowledge_context}"
    )

    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]
    )

    return cast(PatientFollowupAnalysis, response)
