import streamlit as st

def load_css(file_path="assets/style.css"):
    """Loads external CSS styling."""
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

def show_toast(message, icon="✅"):
    """Displays a toast notification in Streamlit."""
    st.toast(message, icon=icon)