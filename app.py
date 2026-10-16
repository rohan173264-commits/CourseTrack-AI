import streamlit as st
import pandas as pd
from config.db_config import fetch_data
from src.utils import load_css

# Page Configuration
st.set_page_config(page_title="CourseTrack AI - Home", page_icon="🎓", layout="wide")
load_css()

# 1. Custom Hero Banner (Professional Look)
st.markdown("""
    <div style='text-align: center; padding: 2rem 0px; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='color: #1E3A8A; font-size: 3rem; margin-bottom: 0;'>🎓 CourseTrack AI</h1>
        <h3 style='color: #4B5563; margin-top: 10px;'>Smart Enquiry Management CRM for Webisoftech</h3>
        <p style='color: #6B7280; font-size: 1.1rem;'>Streamline student admissions, automate lead scoring, and boost your conversion rates.</p>
    </div>
""", unsafe_allow_html=True)

# Fetch Dynamic Data for Metrics
try:
    df = fetch_data("SELECT * FROM enquiries")
    if not df.empty:
        total_enquiries = len(df)
        active_followups = len(df[(df['status'] != 'Converted') & (df['status'] != 'Lost')])
        conversions = len(df[df['status'] == 'Converted'])
    else:
        total_enquiries, active_followups, conversions = 0, 0, 0
except Exception as e:
    total_enquiries, active_followups, conversions = 0, 0, 0

# 2. Key Metrics Section
st.markdown("### 📊 Live System Overview")
m1, m2, m3 = st.columns(3)

with m1:
    st.metric(label="📝 Total Enquiries", value=total_enquiries, delta="All Time")
with m2:
    st.metric(label="🔄 Active Follow-ups", value=active_followups, delta="Pending Tasks", delta_color="off")
with m3:
    st.metric(label="🏆 Total Conversions", value=conversions, delta="Admitted Students")

st.divider()

# 3. Quick Access Module Cards (Replaces plain bullet points)
st.markdown("### 🚀 Quick Access Modules")
st.write("Use the left sidebar navigation to access detailed features, or check module highlights below:")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info("""
    **📊 Dashboard & Analytics**
    \nView high-level metrics, course-wise conversion rates, and visual growth charts.
    """)

with c2:
    st.success("""
    **➕ Add Enquiry**
    \nEnroll new student leads and let the AI automatically assign priority scores.
    """)

with c3:
    st.warning("""
    **🤖 AI Follow-ups**
    \nTrack your pending tasks. AI prioritizes who you should call first today.
    """)

with c4:
    st.error("""
    **🔍 Reports & Search**
    \nFilter student data, search by name/number, and export data directly to CSV.
    """)

# Footer
st.markdown("""
    <div style='text-align: center; margin-top: 50px; color: #9CA3AF; font-size: 0.9rem;'>
        &copy; 2026 Webisoftech. Powered by CourseTrack AI.
    </div>
""", unsafe_allow_html=True)