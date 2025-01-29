import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database import Database
from utils import calculate_statistics, format_currency, format_number
from visualizations import create_time_series, create_earnings_breakdown, create_efficiency_metrics
import os

# Initialize database and directories
db = Database()
exports_dir = "exports"
os.makedirs(exports_dir, exist_ok=True)
backups_dir = "backups"
os.makedirs(backups_dir, exist_ok=True)

# Clear data on startup
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    db.clear_data()  # Start fresh each time

# Page config
st.set_page_config(
    page_title="Rideshare Driver Dashboard",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Rideshare Driver Dashboard")

# Sidebar for data entry and management
with st.sidebar:
    # Data Entry
    with st.form("ride_form"):
        st.subheader("Add New Ride")
        date = st.date_input("Date", value=datetime.now())
        hours = st.number_input("Hours Worked", min_value=0.0, step=0.5)
        miles = st.number_input("Miles Driven", min_value=0.0, step=0.5)
        earnings = st.number_input("Total Earnings ($)", min_value=0.0, step=0.01)

        if st.form_submit_button("Add Entry"):
            db.add_ride(date, hours, miles, earnings)
            st.success("Entry added successfully!")
            st.rerun()

    # Data Management
    st.subheader("Data Management")

    # Save/Load functionality
    save_name = st.text_input("Save/Load Name", placeholder="Enter name")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Save Progress") and save_name:
            db.backup_data(save_name)
            st.success("Progress saved!")

    with col2:
        available_saves = db.get_available_backups()
        if available_saves and st.button("Load Progress"):
            db.restore_data(save_name)
            st.success("Progress loaded!")
            st.rerun()

    # Clear Data
    if st.button("Clear All Data"):
        db.clear_data()
        st.success("All data cleared!")
        st.rerun()

# Main content
col1, col2 = st.columns([2, 1])

# Date range selector
with col1:
    dates = st.date_input(
        "Select Date Range",
        value=(datetime.now() - timedelta(days=30), datetime.now())
    )
    start_date, end_date = dates if len(dates) == 2 else (dates[0], dates[0])

# Load and display data
df = db.get_rides(start_date, end_date)

# Statistics
with col2:
    stats = calculate_statistics(df)
    st.metric("Total Earnings", format_currency(stats['total_earnings']))
    st.metric("Average Hourly Rate", format_currency(stats['avg_hourly_rate']))
    st.metric("Earnings per Mile", format_currency(stats['earnings_per_mile']))

# Data table
st.subheader("Ride History")
if not df.empty:
    edited_df = st.data_editor(
        df.drop(['id', 'created_at'], axis=1),
        column_config={
            "date": "Date",
            "hours": "Hours",
            "miles": "Miles",
            "earnings": "Earnings ($)"
        },
        hide_index=True,
        num_rows="dynamic"
    )
else:
    st.info("No data available for selected date range")

# Visualizations
if not df.empty:
    st.subheader("Analytics")
    viz_col1, viz_col2 = st.columns(2)

    with viz_col1:
        st.plotly_chart(create_earnings_breakdown(df), use_container_width=True)
        st.plotly_chart(create_time_series(df, 'hours', 'Hours Worked Over Time'), use_container_width=True)

    with viz_col2:
        st.plotly_chart(create_efficiency_metrics(df), use_container_width=True)
        st.plotly_chart(create_time_series(df, 'miles', 'Miles Driven Over Time'), use_container_width=True)