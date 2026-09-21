import os
from typing import Any, cast

import httpx
import streamlit as st

API_BASE_URL = os.getenv(
    "MEDICARE_API_URL",
    "http://127.0.0.1:8000",
)


st.set_page_config(
    page_title="MediCare Follow-Up Agent",
    page_icon="🏥",
    layout="wide",
)


def api_get(path: str) -> dict[str, Any]:
    """Call a MediCare API GET endpoint."""
    response = httpx.get(
        f"{API_BASE_URL}{path}",
        timeout=30.0,
    )
    response.raise_for_status()
    return cast(dict[str, Any], response.json())


def api_post(path: str) -> dict[str, Any]:
    """Call a MediCare API POST endpoint."""
    response = httpx.post(
        f"{API_BASE_URL}{path}",
        timeout=120.0,
    )
    response.raise_for_status()
    return cast(dict[str, Any], response.json())


st.title("MediCare Patient Follow-Up Agent")
st.caption(
    "Care-coordination decision support powered by FastAPI, "
    "LangGraph, RAG, MCP and a local LLM."
)

st.divider()

try:
    health = api_get("/health")
    api_status = "Online"
    api_service = health.get(
        "service",
        "MediCare Follow-Up Agent",
    )
except Exception:
    api_status = "Unavailable"
    api_service = "Start the FastAPI service first."

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("API Status", api_status)

with col2:
    st.metric("Service", api_service)

try:
    patients_payload = api_get("/api/v1/patients")
    patients = patients_payload.get("patients", [])
except Exception:
    patients = []

with col3:
    st.metric("Patients", len(patients))

st.divider()

if not patients:
    st.warning(
        "The FastAPI service is unavailable. "
        "Start it with: uv run uvicorn app.main:app --reload"
    )
    st.stop()

patient_options = {
    f"{patient['patient_id']} — {patient['patient_name']}":
        patient["patient_id"]
    for patient in patients
}

selected_label = st.selectbox(
    "Select Patient",
    list(patient_options.keys()),
)

if selected_label is None:
    st.stop()

patient_id = patient_options[selected_label]

try:
    patient = api_get(
        f"/api/v1/patients/{patient_id}"
    )
except Exception as exc:
    st.error(f"Unable to load patient: {exc}")
    st.stop()

st.subheader("Patient Information")

info_col1, info_col2, info_col3, info_col4 = st.columns(4)

with info_col1:
    st.write("**Patient ID**")
    st.write(patient.get("patient_id", "—"))

with info_col2:
    st.write("**Age**")
    st.write(patient.get("age", "—"))

with info_col3:
    st.write("**Gender**")
    st.write(patient.get("gender", "—"))

with info_col4:
    st.write("**Diagnosis**")
    st.write(patient.get("diagnosis", "—"))

details_col1, details_col2 = st.columns(2)

with details_col1:
    st.write("**Medication**")
    st.write(patient.get("current_medication", "—"))

    st.write("**Lab Test**")
    st.write(patient.get("lab_test", "—"))

    st.write("**Lab Value**")
    st.write(
        f"{patient.get('lab_value', '—')} "
        f"{patient.get('lab_unit', '')}"
    )

with details_col2:
    st.write("**Last Visit**")
    st.write(patient.get("last_visit_date", "—"))

    st.write("**Next Scheduled Visit**")
    st.write(patient.get("next_scheduled_visit", "—"))

    st.write("**Days Since Last Visit**")
    st.write(patient.get("days_since_last_visit", "—"))

st.divider()

st.subheader("Follow-Up Workflows")

action_col1, action_col2 = st.columns(2)

with action_col1:
    analyze_clicked = st.button(
        "Run Patient Analysis",
        use_container_width=True,
    )

with action_col2:
    missed_clicked = st.button(
        "Run Missed Appointment Follow-Up",
        use_container_width=True,
    )

if analyze_clicked:
    with st.spinner(
        "Running patient follow-up analysis..."
    ):
        try:
            result = api_post(
                f"/api/v1/workflows/patients/"
                f"{patient_id}/analysis"
            )

            st.success("Patient analysis completed.")

            st.subheader("Analysis")
            st.write(
                result.get(
                    "analysis",
                    "No analysis returned.",
                )
            )

            st.subheader("Recommended Follow-Up Action")
            st.info(
                result.get(
                    "recommended_action",
                    "No recommendation returned.",
                )
            )

        except Exception as exc:
            st.error(f"Analysis failed: {exc}")

if missed_clicked:
    with st.spinner(
        "Checking missed appointment workflow..."
    ):
        try:
            result = api_post(
                f"/api/v1/workflows/patients/"
                f"{patient_id}/missed-appointment"
            )

            st.success(
                "Missed appointment workflow completed."
            )

            st.subheader("Analysis")
            st.write(
                result.get(
                    "analysis",
                    "No analysis returned.",
                )
            )

            st.subheader("Recommended Follow-Up Action")
            st.info(
                result.get(
                    "recommended_action",
                    "No recommendation returned.",
                )
            )

        except Exception as exc:
            st.error(
                f"Missed appointment workflow failed: {exc}"
            )

st.divider()

st.caption(
    "This application provides care-coordination decision "
    "support. It does not diagnose conditions, prescribe "
    "medication, or replace clinical judgment."
)
