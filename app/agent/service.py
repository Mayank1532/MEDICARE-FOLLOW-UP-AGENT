from typing import cast

from app.agent.graph import AgentState, build_followup_graph


def run_agent(patient_id: str, patient_data: dict[str, object]) -> AgentState:
    graph = build_followup_graph()

    result = graph.invoke(
        {
            "patient_id": patient_id,
            "patient_data": patient_data,
        }
    )

    return cast(AgentState, result)
