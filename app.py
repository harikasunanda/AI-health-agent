import streamlit as st
from data import load_data
from agent import analyze_lab

st.set_page_config(
    page_title="AI Healthcare Agent",
    page_icon="🏥",
    layout="wide"
)
st.markdown("""
<h1 style='text-align: center; color: #1f4e79; font-weight: 700;'>
 AI Healthcare Agent
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

selected_speciality = st.sidebar.selectbox(
    "Select Specialty",
    ["All"] + sorted(df["speciality"].dropna().unique().tolist())
)

if selected_speciality != "All":
    df = df[df["speciality"] == selected_speciality]

col1, col2, col3 = st.columns(3)

col1.metric("Total Consultations", len(df))
col2.metric("Unique Doctors", df["doctor_name"].nunique())
col3.metric("Specialties", df["speciality"].nunique())

st.markdown("---")

selected_id = st.selectbox(
    "Select Patient ID",
    df[id_column]
)

selected_data = df[df[id_column] == selected_id]

if selected_data.empty:
    st.error("No data found")
    st.stop()

selected_row = selected_data.iloc[0]

if "history" not in st.session_state:
    st.session_state.history = []


if st.button(" Run AI Analysis"):
    with st.spinner("Analyzing consultation data..."):

        try:
            result = analyze_lab(selected_row.to_dict())

            st.session_state.history.append({
                "id": selected_row[id_column],
                "doctor": selected_row.get("doctor_name", "N/A"),
                "speciality": selected_row.get("speciality", "N/A"),
                "time": selected_row.get("scheduled_at", "N/A"),
                "result": result
            })

            st.success("Analysis Completed")

            st.markdown("###  AI Report")
            st.write(result)

        except Exception as e:
            st.error(f"AI Error: {str(e)}")


st.markdown("---")
st.subheader(" Previous Analysis Reports")

if len(st.session_state.history) == 0:
    st.info("No analysis history available")
else:
    for item in reversed(st.session_state.history):
        with st.expander(f"🧾 {item['id']} | {item['speciality']}"):
            st.write(f"**Doctor:** {item['doctor']}")
            st.write(f"**Time:** {item['time']}")
            st.write("**Analysis:**")
            st.write(item["result"])