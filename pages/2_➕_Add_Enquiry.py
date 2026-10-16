import streamlit as st
from datetime import date
from config.db_config import execute_query
from src.ai_engine import calculate_lead_score
from src.utils import load_css, show_toast

st.set_page_config(page_title="Add Enquiry - CourseTrack AI", layout="wide")
load_css()

st.header("➕ Add New Student Enquiry")

with st.form("add_enquiry_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Student Name*")
        phone = st.text_input("Phone Number*")
        email = st.text_input("Email Address")
        source = st.selectbox("Enquiry Source*",
                              ["WhatsApp", "Instagram", "Facebook", "Phone Call", "Walk-in", "Other"])

    with col2:
        course = st.selectbox("Interested Course*",
                              ["Python Full Stack", "Data Science & AI", "Web Development", "Java Full Stack",
                               "UI/UX Design", "Other"])
        status = st.selectbox("Current Status*",
                              ["New", "Contacted", "Interested", "Demo Attended", "Converted", "Lost"])
        enquiry_dt = st.date_input("Enquiry Date", date.today())
        followup_dt = st.date_input("Next Follow-up Date", date.today())

    notes = st.text_area("Notes / Remarks")

    submit = st.form_submit_button("Save Entry")

    if submit:
        if name and phone:
            # Calculate AI Score
            score, priority = calculate_lead_score(source, status, course)

            # SQLite साठी %s ऐवजी ? वापरले आहे
            sql = """INSERT INTO enquiries
                     (student_name, phone, email, source, course, status, enquiry_date, next_followup_date, notes, \
                      lead_score, ai_priority)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

            val = (name, phone, email, source, course, status, str(enquiry_dt), str(followup_dt), notes, score,
                   priority)

            if execute_query(sql, val):
                show_toast(f"Student Registered! Priority: {priority}", icon="🚀")
                st.success(f"Enquiry saved successfully! **AI Lead Score:** {score}/100 | **Priority:** {priority}")
        else:
            st.error("Name and Phone Number are required fields.")