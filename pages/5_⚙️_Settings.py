import streamlit as st
import json
from config.db_config import fetch_data
from src.utils import load_css

st.set_page_config(page_title="Settings - CourseTrack AI", layout="wide")
load_css()

st.header("⚙️ System Settings & Database Backup")

st.subheader("💾 System Backup")
st.write("Download a secure backup of the database in JSON format.")

if st.button("Generate Data Backup (Export Data)"):
    df = fetch_data("SELECT * FROM enquiries")
    if not df.empty:
        json_data = df.to_json(orient="records", date_format="iso")
        st.download_button(
            label="📥 Download JSON Backup",
            data=json_data,
            file_name="coursetrack_backup.json",
            mime="application/json"
        )
    else:
        st.warning("No data available to backup.")