import streamlit as st
from data import load_data
from agent import analyze_lab_results as analyze_lab

# -------------------------------
# Page Config
# -------------------------------
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


st.sidebar.header("Filters")

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
    "Select Application ID",
    df["application_id"]
)

selected_data = df[df["application_id"] == selected_id]

if selected_data.empty:
    st.error("No data found")
    st.stop()

selected_row = selected_data.iloc[0]

if "history" not in st.session_state:
    st.session_state.history = []


if st.button("Run AI Analysis"):
    with st.spinner("Analyzing data..."):

        result = analyze_lab(selected_row.to_dict())

        st.session_state.history.append({
            "application_id": selected_row["application_id"],
            "doctor": selected_row["doctor_name"],
            "speciality": selected_row["speciality"],
            "time": selected_row["scheduled_at"],
            "result": result
        })

        st.success("Analysis Completed")
        st.markdown("###  AI Report")
        st.write(result)


st.markdown("---")
st.subheader(" Previous Analysis Reports")

if len(st.session_state.history) == 0:
    st.info("No analysis history available")
else:
    for item in reversed(st.session_state.history):
        with st.expander(f"🧾 {item['application_id']} | {item['speciality']}"):
            st.write(f"**Doctor:** {item['doctor']}")
            st.write(f"**Time:** {item['time']}")
            st.write("**Analysis:**")
            st.write(item["result"])

