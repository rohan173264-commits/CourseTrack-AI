import sqlite3
import pandas as pd
import streamlit as st

DB_NAME = "coursetrack_ai.db"

def get_db_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_sqlite_db():
    """Creates the table automatically if it does not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enquiries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        source TEXT NOT NULL,
        course TEXT NOT NULL,
        status TEXT DEFAULT 'New',
        enquiry_date DATE NOT NULL,
        next_followup_date DATE,
        notes TEXT,
        lead_score INTEGER DEFAULT 50,
        ai_priority TEXT DEFAULT 'Medium',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()

# Initialize the database table when the app runs
init_sqlite_db()

def fetch_data(query, params=None):
    """Executes a SELECT query to retrieve data."""
    conn = get_db_connection()
    try:
        df = pd.read_sql(query, conn, params=params)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        df = pd.DataFrame()
    finally:
        conn.close()
    return df

def execute_query(query, params=None):
    """Executes INSERT, UPDATE, or DELETE queries."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return False
    finally:
        conn.close()