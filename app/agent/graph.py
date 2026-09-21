from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from app.llm.patient_analysis import analyze_patient_with_llm


class AgentState(TypedDict, total=False):
    patient_id: str
    patient_data: dict[str, object]
    analysis: str
    recommended_action: str


def build_followup_graph() -> Any:
    graph = StateGraph(AgentState)

    graph.add_node("prepare_patient", prepare_patient)
    graph.add_node("analyze_patient", analyze_patient)

    graph.add_edge(START, "prepare_patient")
    graph.add_edge("prepare_patient", "analyze_patient")
    graph.add_edge("analyze_patient", END)

    return graph.compile()


def prepare_patient(state: AgentState) -> AgentState:
    return {
        **state,
        "analysis": "",
        "recommended_action": "",
    }


def analyze_patient(state: AgentState) -> AgentState:
    patient = state.get("patient_data", {})
    llm_result = analyze_patient_with_llm(patient)

    return {
        **state,
        "analysis": llm_result.analysis,
        "recommended_action": llm_result.recommended_action,
    }
