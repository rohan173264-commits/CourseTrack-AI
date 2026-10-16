import streamlit as st
import pandas as pd
import plotly.express as px
from config.db_config import fetch_data
from src.utils import load_css

st.set_page_config(page_title="Dashboard - CourseTrack AI", layout="wide")
load_css()

st.header("📊 Executive Dashboard & Analytics")

df = fetch_data("SELECT * FROM enquiries")

if df.empty:
    st.info("No enquiry data available yet. Please add enquiries to view analytics.")
else:
    # Key Metrics
    total = len(df)
    converted = len(df[df['status'] == 'Converted'])
    conversion_rate = (converted / total) * 100 if total > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Enquiries", total)
    col2.metric("Converted Students", converted)
    col3.metric("Conversion Rate", f"{conversion_rate:.2f}%")

    st.divider()

    # Visual Analytics Row 1
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("📚 Course-wise Enquiries")
        course_df = df['course'].value_counts().reset_index()
        course_df.columns = ['Course', 'Count']
        fig_course = px.bar(course_df, x='Course', y='Count', color='Course', text='Count')
        st.plotly_chart(fig_course, use_container_width=True)

    with c2:
        st.subheader("🌐 Source-wise Enquiries")
        source_df = df['source'].value_counts().reset_index()
        source_df.columns = ['Source', 'Count']
        fig_source = px.pie(source_df, names='Source', values='Count', hole=0.4)
        st.plotly_chart(fig_source, use_container_width=True)

    # Visual Analytics Row 2: Monthly Trends
    st.subheader("📈 Monthly Enquiry & Admission Trends")
    df['enquiry_date'] = pd.to_datetime(df['enquiry_date'])
    df['Month'] = df['enquiry_date'].dt.to_period('M').astype(str)

    trend_df = df.groupby(['Month', 'status']).size().reset_index(name='Count')
    fig_trend = px.line(trend_df, x='Month', y='Count', color='status', markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)