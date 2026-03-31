import streamlit as st
import pandas as pd
from data import load_data
from agent import analyze_lab

st.set_page_config(
    page_title="AI HealthCare Agent",
    page_icon="🏥",
    layout="wide"
)

st.markdown("""
<h1 style='text-align: center; color: #1f4e79; font-weight: 700;'>
 AI HealthCare Agent
</h1>
<hr>
""", unsafe_allow_html=True)

df = load_data()

if df.empty:
    st.error("Failed to load data")
    st.stop()

df.columns = df.columns.str.strip().str.lower()

id_column = "patient_id" if "patient_id" in df.columns else "application_id"

st.sidebar.header(" Filters")

selected_gender = st.sidebar.selectbox(
    "Select Gender",
    ["All"] + sorted(df["patient_gender"].dropna().unique().tolist())
)

if selected_gender != "All":
    df = df[df["patient_gender"] == selected_gender]

col1, col2, col3 = st.columns(3)

col1.metric("Total Patients", len(df))

age_series = pd.to_numeric(df["patient_age"], errors="coerce")
avg_age = age_series.mean()
col2.metric("Avg Age", int(avg_age) if pd.notna(avg_age) else "N/A")

bmi_series = pd.to_numeric(df["bmi"], errors="coerce")
avg_bmi = bmi_series.mean()
col3.metric("Avg BMI", round(avg_bmi, 2) if pd.notna(avg_bmi) else "N/A")

st.markdown("---")

selected_id = st.selectbox(
    "Select Patient ID",
    df[id_column]
)

selected_data = df[df["patient_id"] == selected_id]

if selected_data.empty:
    st.error("No data found")
    st.stop()

selected_row = selected_data.iloc[0]

st.subheader(" Patient Information")

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Name:** {selected_row.get('patient_name', 'N/A')}")
    st.write(f"**Age:** {selected_row.get('patient_age', 'N/A')}")
    st.write(f"**Gender:** {selected_row.get('patient_gender', 'N/A')}")

with col2:
    st.write(f"**BMI:** {selected_row.get('bmi', 'N/A')}")
    st.write(f"**BP:** {selected_row.get('systolic_bp', 'N/A')}/{selected_row.get('diastolic_bp', 'N/A')}")
    st.write(f"**Pulse:** {selected_row.get('pulse', 'N/A')}")
    st.write(f"**SpO2:** {selected_row.get('spo2', 'N/A')}")
    st.write(f"**Temperature:** {selected_row.get('temperature', 'N/A')}")

st.markdown("---")

st.subheader(" Symptoms & Lab Results")

st.write(f"**Symptoms:** {selected_row.get('doctorsymptoms', 'N/A')}")
st.write(f"**Lab Results:** {selected_row.get('labtestresult', 'N/A')}")

if "history" not in st.session_state:
    st.session_state.history = []

if st.button(" Run AI Diagnosis"):
    with st.spinner("Analyzing patient data..."):

        try:
            result = analyze_lab(selected_row.to_dict())

            st.session_state.history.append({
                "patient_id": selected_row.get("patient_id"),
                "name": selected_row.get("patient_name"),
                "result": result
            })

            st.success("Diagnosis Completed")

            st.markdown("###  AI Diagnosis Report")
            st.write(result)

        except Exception as e:
            st.error(f"AI Error: {str(e)}")

st.markdown("---")
st.subheader(" Previous Reports")

if len(st.session_state.history) == 0:
    st.info("No reports available")
else:
    for item in reversed(st.session_state.history):
        with st.expander(f" {item['patient_id']} | {item['name']}"):
            st.write(item["result"])