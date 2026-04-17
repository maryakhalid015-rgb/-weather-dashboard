import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(page_title="UAE Weather Dashboard", layout="wide")

# ===== THEME =====
current_hour = datetime.now().hour
if 6 <= current_hour < 17:
    theme_mode = "day"
elif 17 <= current_hour < 19:
    theme_mode = "sunset"
else:
    theme_mode = "night"

def get_theme(mode):
    if mode == "day":
        return {"app_bg_css": "background: linear-gradient(180deg, #1a4a7a 0%, #2563a8 25%, #3b82c4 55%, #5ba3d9 80%, #7ec8e3 100%);", "card_bg": "rgba(255,255,255,0.12)", "text": "#ffffff", "muted": "rgba(255,255,255,0.75)"}
    elif mode == "sunset":
        return {"app_bg_css": "background: linear-gradient(180deg, #0f0c29 0%, #302b63 20%, #6b3a8a 40%, #c0534a 65%, #e8753a 82%, #f4a24e 100%);", "card_bg": "rgba(15,12,41,0.45)", "text": "#ffffff", "muted": "rgba(255,255,255,0.75)"}
    else:
        return {"app_bg_css": "background: linear-gradient(180deg, #07111f 0%, #0a1a30 20%, #0e2340 45%, #122b50 70%, #163660 100%);", "card_bg": "rgba(255,255,255,0.08)", "text": "#ffffff", "muted": "rgba(255,255,255,0.65)"}

theme = get_theme(theme_mode)
st.markdown(f"<style>.stApp {{{theme['app_bg_css']} color: {theme['text']};}} .glass-card {{background: {theme['card_bg']}; border-radius: 20px; padding: 20px;}}</style>", unsafe_allow_html=True)

st.title("🌤️ UAE Weather Dashboard")

if not os.path.exists("weather_data.csv"):
    st.warning("⚠️ weather_data.csv not found")
else:
    df = pd.read_csv("weather_data.csv", on_bad_lines="skip")
    if not df.empty:
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Latest Temperature", df.iloc[-1].get("temp_c", "-"), "°C")
        with col2:
            st.metric("Humidity", df.iloc[-1].get("humidity", "-"), "%")
        
        st.write("### Weather Data")
        st.dataframe(df.tail(10))
        
        col1, col2 = st.columns(2)
        with col1:
            if "temp_c" in df.columns and len(df) > 1:
                fig = go.Figure()
                fig.add_trace(go.Scatter(y=df["temp_c"], mode="lines", name="Temperature"))
                fig.update_layout(height=300, title="Temperature Trend")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if "humidity" in df.columns and len(df) > 1:
                fig = go.Figure()
                fig.add_trace(go.Scatter(y=df["humidity"], mode="lines", name="Humidity"))
                fig.update_layout(height=300, title="Humidity Trend")
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available yet")
