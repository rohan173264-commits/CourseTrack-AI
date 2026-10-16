from datetime import date
import pandas as pd
import streamlit as st
from config.db_config import fetch_data
from src.utils import load_css

st.set_page_config(page_title="Reports - CourseTrack AI", layout="wide")
load_css()

st.header("🔍 Advanced Search & Export Reports")

# Fetch all data from database
df = fetch_data("SELECT * FROM enquiries")

if df.empty:
  st.info(
      "No enquiry records found in the database. Please add enquiries first."
  )
else:
  # Filters UI
  col1, col2, col3 = st.columns(3)
  with col1:
    search = st.text_input("Search Name or Phone")
  with col2:
    courses = st.multiselect("Filter By Course", df["course"].unique())
  with col3:
    statuses = st.multiselect("Filter By Status", df["status"].unique())

  filtered = df.copy()

  if search:
    filtered = filtered[
        filtered["student_name"].str.contains(search, case=False, na=False)
        | filtered["phone"].astype(str).str.contains(search, case=False, na=False)
    ]

  if courses:
    filtered = filtered[filtered["course"].isin(courses)]

  if statuses:
    filtered = filtered[filtered["status"].isin(statuses)]

  st.divider()

  # Display Data Table
  st.subheader(f"📋 Records Found ({len(filtered)})")
  st.dataframe(filtered, use_container_width=True)

  # CSV Download Button (Always Visible when data exists)
  csv_data = filtered.to_csv(index=False).encode("utf-8")
  st.download_button(
      label="📥 Download Filtered CSV Report",
      data=csv_data,
      file_name=f"enquiries_report_{date.today()}.csv",
      mime="text/csv",
      use_container_width=True,
  )