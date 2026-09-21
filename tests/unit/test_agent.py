from app.agent.graph import build_followup_graph
from app.llm.patient_analysis import PatientFollowupAnalysis


def test_followup_graph_uses_llm(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_llm(patient_data: dict[str, object]) -> PatientFollowupAnalysis:
        captured["patient_data"] = patient_data

        return PatientFollowupAnalysis(
            analysis="Follow-up review required based on the supplied record.",
            recommended_action="Schedule care-team follow-up.",
        )

    monkeypatch.setattr(
        "app.agent.graph.analyze_patient_with_llm",
        fake_llm,
    )

    patient_data = {
        "diagnosis": "Hypertension",
        "age": 58,
        "missed_last_appointment": "Yes",
    }

    graph = build_followup_graph()

    result = graph.invoke(
        {
            "patient_id": "P0001",
            "patient_data": patient_data,
        }
    )

    assert result["patient_id"] == "P0001"
    assert result["patient_data"] == patient_data
    assert result["analysis"] == (
        "Follow-up review required based on the supplied record."
    )
    assert result["recommended_action"] == "Schedule care-team follow-up."
    assert captured["patient_data"] == patient_data


def test_followup_graph_preserves_patient_identity(monkeypatch) -> None:
    def fake_llm(patient_data: dict[str, object]) -> PatientFollowupAnalysis:
        return PatientFollowupAnalysis(
            analysis="Analysis generated from patient record.",
            recommended_action="Review with care team.",
        )

    monkeypatch.setattr(
        "app.agent.graph.analyze_patient_with_llm",
        fake_llm,
    )

    graph = build_followup_graph()

    result = graph.invoke(
        {
            "patient_id": "P0042",
            "patient_data": {
                "diagnosis": "Diabetes",
            },
        }
    )

    assert result["patient_id"] == "P0042"
    assert result["analysis"] == "Analysis generated from patient record."
    assert result["recommended_action"] == "Review with care team."
