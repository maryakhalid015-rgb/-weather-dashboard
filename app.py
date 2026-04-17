import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="UAE Weather Dashboard", layout="wide")
st.title("🌤️ UAE Weather Dashboard")

# Check if data file exists
if not os.path.exists("weather_data.csv"):
    st.error("❌ weather_data.csv not found. Please ensure the file is uploaded.")
    st.stop()

# Load data
try:
    df = pd.read_csv("weather_data.csv", on_bad_lines="skip")
except Exception as e:
    st.error(f"Error reading CSV: {e}")
    st.stop()

if df.empty:
    st.warning("⚠️ CSV file is empty. Waiting for data...")
    st.stop()

# Display latest data
st.subheader("Latest Reading")
latest = df.iloc[-1]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Temperature", f"{latest.get('temp_c', '-')}°C")
with col2:
    st.metric("Humidity", f"{latest.get('humidity', '-')}%")
with col3:
    st.metric("Wind Speed", f"{latest.get('wind_kph', '-')} km/h")
with col4:
    st.metric("Pressure", f"{latest.get('pressure_mb', '-')} mb")

# Display table
st.subheader("Recent Data (Last 10 Records)")
st.dataframe(df.tail(10), use_container_width=True)

# Display all cities
if "city" in df.columns:
    st.subheader("Cities in Database")
    cities = df["city"].unique()
    st.write(f"**Total cities: {len(cities)}**")
    st.write(cities)

# Export button
st.subheader("Export Data")
csv = df.to_csv(index=False)
st.download_button(
    label="📥 Download All Data as CSV",
    data=csv,
    file_name="weather_data.csv",
    mime="text/csv"
)

st.success("✅ Dashboard is working!")
