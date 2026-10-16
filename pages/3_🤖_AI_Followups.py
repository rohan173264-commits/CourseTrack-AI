from datetime import date
import urllib.parse
import pandas as pd
import streamlit as st
from config.db_config import execute_query, fetch_data
from src.utils import load_css, show_toast

st.set_page_config(page_title="AI Followups - CourseTrack AI", layout="wide")
load_css()

st.header("🤖 AI-Driven Follow-up Tracker")

today = str(date.today())

# 1. Fixed SQLite placeholder syntax (? instead of %s) and query parameter tuple
query = "SELECT * FROM enquiries WHERE next_followup_date <= ? AND status NOT IN ('Converted', 'Lost') ORDER BY lead_score DESC"
df_pending = fetch_data(query, (today,))

if df_pending.empty:
  st.success("🎉 No pending follow-ups today!")
else:
  st.warning(
      f"⚠️ You have **{len(df_pending)}** pending follow-ups prioritized by AI"
      " Lead Score."
  )

  # Render Pending Table
  st.dataframe(
      df_pending[[
          "id",
          "student_name",
          "phone",
          "course",
          "source",
          "status",
          "lead_score",
          "ai_priority",
          "next_followup_date",
          "notes",
      ]],
      use_container_width=True,
  )

  st.divider()
  st.subheader("⚡ Quick Status Update & Action")

  selected_id = st.selectbox("Select Student ID", df_pending["id"].tolist())
  student_data = df_pending[df_pending["id"] == selected_id].iloc[0]

  # 2. Fixed key casing ('phone', 'lead_score') and object variable name
  st.info(
      f"**Selected:** {student_data['student_name']} | **Phone:**"
      f" {student_data['phone']} | **AI Score:** {student_data['lead_score']}"
  )

  # 3. Wrapped inside st.form for seamless updates
  with st.form("update_followup_form", clear_on_submit=False):
    col1, col2 = st.columns(2)

    with col1:
      status_list = [
          "Contacted",
          "Interested",
          "Demo Attended",
          "Converted",
          "Lost",
      ]
      curr_idx = (
          status_list.index(student_data["status"])
          if student_data["status"] in status_list
          else 0
      )
      new_status = st.selectbox("New Status", status_list, index=curr_idx)

    with col2:
      new_date = st.date_input("Next Follow-up Date", date.today())

    # 4. Changed date_input to text_area for notes
    u_notes = st.text_area("Updated Notes", str(student_data["notes"] or ""))

    submit_btn = st.form_submit_button("Update Enquiry")

    if submit_btn:
      # 5. Fixed table typo ('enquiries') and placeholders (?)
      update_sql = (
          "UPDATE enquiries SET status=?, next_followup_date=?, notes=? WHERE"
          " id=?"
      )
      if execute_query(
          update_sql, (new_status, str(new_date), u_notes, selected_id)
      ):
        show_toast("Status updated successfully!", icon="✅")
        st.rerun()

  st.divider()

  # Action: Direct WhatsApp Feature
  phone_num = (
      str(student_data["phone"]).strip().replace(" ", "").replace("+", "")
  )
  if len(phone_num) == 10:
    phone_num = "91" + phone_num

  msg = (
      f"Hello {student_data['student_name']}, following up regarding your"
      f" enquiry for the {student_data['course']} course at Webisoftech."
  )
  whatsapp_url = (
      f"https://wa.me/{phone_num}?text={urllib.parse.quote(msg)}"
  )
  st.link_button("📲 Send WhatsApp Message", whatsapp_url)