import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(page_title="UAE Weather Dashboard", layout="wide")

# ================= TIME-BASED THEME =================
current_hour = datetime.now().hour

if 6 <= current_hour < 17:
    theme_mode = "day"
elif 17 <= current_hour < 19:
    theme_mode = "sunset"
else:
    theme_mode = "night"


def get_theme(mode):
    if mode == "day":
        return {
            "app_bg_css": """
                background: linear-gradient(180deg,
                    #1a4a7a 0%, #2563a8 25%, #3b82c4 55%, #5ba3d9 80%, #7ec8e3 100%
                );
            """,
            "card_bg":  "rgba(255,255,255,0.12)",
            "small_bg": "rgba(255,255,255,0.10)",
            "hero_bg":  "rgba(255,255,255,0.08)",
            "text":      "#ffffff",
            "muted":     "rgba(255,255,255,0.75)",
            "soft_text": "rgba(255,255,255,0.55)",
            "pill_bg":   "rgba(255,255,255,0.15)",
            "pill_text": "#ffffff",
            "border":    "rgba(255,255,255,0.18)",
            "plot_bg":   "rgba(255,255,255,0.05)",
            "grid":      "rgba(255,255,255,0.10)",
            "shadow":    "0 8px 32px rgba(0,0,0,0.18)",
            "sky_object": "☀️",
            "accent":    "#7dd3fc",
            "atmospheric_css": "",
        }
    elif mode == "sunset":
        return {
            "app_bg_css": """
                background: linear-gradient(180deg,
                    #0f0c29 0%, #302b63 20%, #6b3a8a 40%,
                    #c0534a 65%, #e8753a 82%, #f4a24e 100%
                );
            """,
            "card_bg":  "rgba(15,12,41,0.45)",
            "small_bg": "rgba(15,12,41,0.40)",
            "hero_bg":  "rgba(15,12,41,0.35)",
            "text":      "#ffffff",
            "muted":     "rgba(255,255,255,0.75)",
            "soft_text": "rgba(255,255,255,0.50)",
            "pill_bg":   "rgba(255,255,255,0.12)",
            "pill_text": "#ffe4cc",
            "border":    "rgba(255,255,255,0.14)",
            "plot_bg":   "rgba(15,12,41,0.30)",
            "grid":      "rgba(255,255,255,0.08)",
            "shadow":    "0 8px 32px rgba(0,0,0,0.30)",
            "sky_object": "🌤️",
            "accent":    "#fbbf24",
            "atmospheric_css": "",
        }
    else:  # night
        return {
            "app_bg_css": """
                background: linear-gradient(180deg,
                    #07111f 0%, #0a1a30 20%, #0e2340 45%,
                    #122b50 70%, #163660 100%
                );
            """,
            "card_bg":  "rgba(255,255,255,0.08)",
            "small_bg": "rgba(255,255,255,0.07)",
            "hero_bg":  "rgba(255,255,255,0.06)",
            "text":      "#ffffff",
            "muted":     "rgba(255,255,255,0.65)",
            "soft_text": "rgba(255,255,255,0.40)",
            "pill_bg":   "rgba(255,255,255,0.10)",
            "pill_text": "#bfdbfe",
            "border":    "rgba(255,255,255,0.12)",
            "plot_bg":   "rgba(0,0,0,0.20)",
            "grid":      "rgba(255,255,255,0.07)",
            "shadow":    "0 8px 32px rgba(0,0,0,0.40)",
            "sky_object": "🌙",
            "accent":    "#93c5fd",
            "atmospheric_css": """
@keyframes twinkle  { 0%,100%{opacity:.9;transform:scale(1)}  50%{opacity:.2;transform:scale(.65)} }
@keyframes twinkle2 { 0%,100%{opacity:.7;transform:scale(1)}  50%{opacity:.1;transform:scale(.55)} }
.stApp::before {
    content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
    background-image:
        radial-gradient(1.8px 1.8px at  42px  38px,rgba(255,255,255,.95),transparent),
        radial-gradient(1.5px 1.5px at 148px  72px,rgba(255,255,255,.85),transparent),
        radial-gradient(2.0px 2.0px at 290px 120px,rgba(255,255,255,.90),transparent),
        radial-gradient(1.6px 1.6px at 460px  55px,rgba(255,255,255,.80),transparent),
        radial-gradient(1.8px 1.8px at 620px 140px,rgba(255,255,255,.88),transparent),
        radial-gradient(1.5px 1.5px at 810px  80px,rgba(255,255,255,.75),transparent),
        radial-gradient(2.0px 2.0px at 980px 110px,rgba(255,255,255,.92),transparent),
        radial-gradient(1.6px 1.6px at1140px  65px,rgba(255,255,255,.82),transparent),
        radial-gradient(1.8px 1.8px at1350px  95px,rgba(255,255,255,.78),transparent),
        radial-gradient(1.5px 1.5px at  95px 185px,rgba(255,255,255,.70),transparent),
        radial-gradient(1.6px 1.6px at 340px 200px,rgba(255,255,255,.80),transparent),
        radial-gradient(1.8px 1.8px at 540px 210px,rgba(255,255,255,.72),transparent),
        radial-gradient(1.5px 1.5px at 760px 175px,rgba(255,255,255,.85),transparent),
        radial-gradient(2.0px 2.0px at 920px 220px,rgba(255,255,255,.90),transparent),
        radial-gradient(1.6px 1.6px at1100px 190px,rgba(255,255,255,.76),transparent),
        radial-gradient(1.2px 1.2px at  68px 145px,rgba(255,255,255,.60),transparent),
        radial-gradient(1.0px 1.0px at 200px  30px,rgba(255,255,255,.55),transparent),
        radial-gradient(1.2px 1.2px at 410px 160px,rgba(255,255,255,.65),transparent),
        radial-gradient(1.0px 1.0px at 700px  40px,rgba(255,255,255,.58),transparent),
        radial-gradient(1.2px 1.2px at 870px 155px,rgba(255,255,255,.62),transparent),
        radial-gradient(1.0px 1.0px at1060px 130px,rgba(255,255,255,.50),transparent),
        radial-gradient(1.2px 1.2px at1260px 180px,rgba(255,255,255,.60),transparent),
        radial-gradient(1.0px 1.0px at 175px 250px,rgba(255,255,255,.55),transparent),
        radial-gradient(1.2px 1.2px at 480px 270px,rgba(255,255,255,.60),transparent),
        radial-gradient(1.0px 1.0px at 660px 240px,rgba(255,255,255,.52),transparent),
        radial-gradient(1.2px 1.2px at1000px 255px,rgba(255,255,255,.58),transparent);
    background-repeat:repeat;
    animation:twinkle 3.8s ease-in-out infinite;
}
.stApp::after {
    content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
    background-image:
        radial-gradient(1.4px 1.4px at 130px  95px,rgba(200,220,255,.70),transparent),
        radial-gradient(1.2px 1.2px at 320px  50px,rgba(200,220,255,.55),transparent),
        radial-gradient(1.5px 1.5px at 570px 100px,rgba(200,220,255,.65),transparent),
        radial-gradient(1.3px 1.3px at 730px  70px,rgba(200,220,255,.60),transparent),
        radial-gradient(1.4px 1.4px at 890px 115px,rgba(200,220,255,.68),transparent),
        radial-gradient(1.2px 1.2px at1050px  85px,rgba(200,220,255,.50),transparent),
        radial-gradient(1.5px 1.5px at1200px 130px,rgba(200,220,255,.62),transparent),
        radial-gradient(1.3px 1.3px at  50px 230px,rgba(200,220,255,.48),transparent),
        radial-gradient(1.4px 1.4px at 250px 280px,rgba(200,220,255,.55),transparent),
        radial-gradient(1.2px 1.2px at 450px 300px,rgba(200,220,255,.52),transparent),
        radial-gradient(1.5px 1.5px at 800px 290px,rgba(200,220,255,.60),transparent),
        radial-gradient(1.3px 1.3px at1150px 270px,rgba(200,220,255,.48),transparent);
    background-repeat:repeat;
    animation:twinkle2 5.2s ease-in-out infinite 1.3s;
}
""",
        }


theme = get_theme(theme_mode)


# ================= HELPERS =================
def get_weather_icon(condition, mode):
    if not isinstance(condition, str):
        return theme["sky_object"]
    c = condition.lower()
    if "sun" in c or "clear" in c:
        return "☀️" if mode == "day" else "🌙"
    elif "cloud" in c or "overcast" in c:
        return "⛅" if mode == "day" else "☁️"
    elif "rain" in c or "drizzle" in c:
        return "🌧️"
    elif "thunder" in c or "storm" in c:
        return "⛈️"
    elif "fog" in c or "mist" in c:
        return "🌫️"
    elif "wind" in c:
        return "💨"
    return theme["sky_object"]


def interpret_humidity(h):
    if pd.isna(h): return "No data"
    elif h < 30:   return "Low humidity"
    elif h <= 60:  return "Comfortable"
    else:          return "High humidity"


def interpret_uv(u):
    if pd.isna(u): return "No data"
    elif u < 3:    return "Low"
    elif u < 6:    return "Moderate"
    elif u < 8:    return "High"
    else:          return "Very high"


def interpret_wind(w):
    if pd.isna(w): return "No data"
    elif w < 10:   return "Light breeze"
    elif w < 25:   return "Moderate"
    else:          return "Strong winds"


def interpret_pressure(p):
    if pd.isna(p): return "No data"
    elif p < 1005: return "Low pressure"
    elif p <= 1020: return "Normal"
    else:          return "High pressure"


city_coordinates = {
    "Ajman":          {"lat": 25.4052, "lon": 55.5136},
    "Dubai":          {"lat": 25.2048, "lon": 55.2708},
    "Sharjah":        {"lat": 25.3463, "lon": 55.4209},
    "Abu Dhabi":      {"lat": 24.4539, "lon": 54.3773},
    "Umm Al Quwain":  {"lat": 25.5647, "lon": 55.5552},
    "Fujairah":       {"lat": 25.1288, "lon": 56.3265},
    "Ras Al Khaimah": {"lat": 25.8007, "lon": 55.9762},
}


def apply_chart_style(fig, title, x_title, y_title):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=theme["plot_bg"],
        title=dict(text=title, font=dict(color=theme["text"], size=14)),
        height=320,
        font=dict(color=theme["muted"]),
        legend=dict(orientation="h", y=1.08, x=0, font=dict(color=theme["muted"], size=11)),
        margin=dict(l=10, r=10, t=46, b=10),
    )
    fig.update_xaxes(
        title_text=x_title, title_font=dict(color=theme["soft_text"], size=10),
        tickfont=dict(color=theme["soft_text"], size=9),
        showgrid=False, zeroline=False, showline=False
    )
    fig.update_yaxes(
        title_text=y_title, title_font=dict(color=theme["soft_text"], size=10),
        tickfont=dict(color=theme["soft_text"], size=9),
        showgrid=True, gridcolor=theme["grid"], zeroline=False, showline=False
    )
    return fig


# ================= CSS =================
st.markdown(f"""
<style>
html, body, [class*="css"] {{
    font-family: -apple-system, 'SF Pro Display', 'Inter', 'Segoe UI', sans-serif;
}}
.stApp {{
    {theme["app_bg_css"]}
    color: {theme["text"]};
    min-height: 100vh;
}}
{theme["atmospheric_css"]}
.block-container {{
    position: relative;
    z-index: 1;
    padding-top: 1.6rem;
}}
.dash-title {{
    font-size: 30px;
    font-weight: 300;
    color: #ffffff;
    letter-spacing: -0.5px;
    line-height: 1.2;
}}
.dash-subtitle {{
    font-size: 11px;
    font-weight: 500;
    color: {theme["soft_text"]};
    margin-top: 3px;
    text-transform: uppercase;
    letter-spacing: 0.10em;
}}
.dash-mode-badge {{
    display: inline-block;
    background: rgba(255,255,255,0.09);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 11px;
    color: {theme["muted"]};
    margin-top: 6px;
    font-weight: 500;
}}
.glass-card {{
    background: {theme["card_bg"]};
    border: 1px solid {theme["border"]};
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 20px 22px;
    box-shadow: {theme["shadow"]};
}}
.hero-card {{
    background: {theme["hero_bg"]};
    border: 1px solid {theme["border"]};
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border-radius: 24px;
    padding: 28px;
    min-height: 270px;
    box-shadow: {theme["shadow"]};
    position: relative;
    overflow: hidden;
}}
.small-card {{
    background: {theme["small_bg"]};
    border: 1px solid {theme["border"]};
    border-radius: 18px;
    padding: 16px 18px;
    min-height: 105px;
    box-shadow: {theme["shadow"]};
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    margin-bottom: 10px;
}}
.metric-label {{
    color: {theme["muted"]};
    font-size: 11px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 5px;
}}
.metric-big   {{ color:#fff; font-size:30px; font-weight:600; letter-spacing:-0.5px; }}
.metric-mid   {{ color:#fff; font-size:22px; font-weight:500; letter-spacing:-0.3px; margin:4px 0; }}
.metric-note  {{ color:{theme["muted"]}; font-size:12px; font-weight:400; margin-top:3px; }}
.section-title {{
    color: rgba(255,255,255,0.85);
    font-size: 11px;
    font-weight: 600;
    margin-top: 22px;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 0.10em;
}}
.weather-condition {{
    color: {theme["muted"]};
    font-size: 17px;
    font-weight: 400;
    margin-top: 4px;
}}
.city-badge {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(255,255,255,0.12);
    color: rgba(255,255,255,0.90);
    padding: 5px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 16px;
    border: 1px solid rgba(255,255,255,0.16);
}}
.info-pill {{
    display: inline-block;
    background: {theme["pill_bg"]};
    color: {theme["pill_text"]};
    padding: 4px 11px;
    border-radius: 999px;
    font-size: 11px;
    margin-right: 5px;
    margin-top: 8px;
    border: 1px solid {theme["border"]};
    font-weight: 500;
}}
hr.divider {{
    border:none; height:1px;
    background:{theme["border"]}; margin:13px 0;
}}
div[data-testid="stMetric"] {{
    background: {theme["small_bg"]};
    border: 1px solid {theme["border"]};
    padding: 13px 15px;
    border-radius: 16px;
    box-shadow: {theme["shadow"]};
    backdrop-filter: blur(16px);
}}
div[data-testid="stMetricLabel"] > div {{
    color: {theme["muted"]} !important;
    font-size: 10px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}}
div[data-testid="stMetricValue"] > div {{
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 20px !important;
}}
label, .stSelectbox label {{
    color: {theme["muted"]} !important;
    font-weight: 600 !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}}
div[data-baseweb="select"] > div {{
    background: {theme["small_bg"]} !important;
    border: 1px solid {theme["border"]} !important;
    border-radius: 12px !important;
    color: {theme["text"]} !important;
    backdrop-filter: blur(16px) !important;
}}
div[data-baseweb="select"] * {{ color: {theme["text"]} !important; }}
.stInfo {{
    background: {theme["small_bg"]} !important;
    color: {theme["text"]} !important;
    border: 1px solid {theme["border"]} !important;
    border-radius: 12px !important;
}}
.alert-badge {{
    display:inline-block;
    background:rgba(239,68,68,0.18); color:#fca5a5;
    border:1px solid rgba(239,68,68,0.28);
    border-radius:8px; padding:6px 12px;
    font-size:13px; font-weight:500;
}}
.no-alert-badge {{
    display:inline-block;
    background:rgba(34,197,94,0.14); color:#86efac;
    border:1px solid rgba(34,197,94,0.24);
    border-radius:8px; padding:6px 12px;
    font-size:13px; font-weight:500;
}}
.insight-row {{
    display:flex; align-items:flex-start; gap:10px;
    padding:9px 0;
    border-bottom:1px solid {theme["border"]};
    font-size:14px; color:rgba(255,255,255,0.82);
    font-weight:400; line-height:1.5;
}}
.insight-row:last-child {{ border-bottom:none; }}

.pipeline-bar {{
    display: flex;
    align-items: center;
    gap: 20px;
    flex-wrap: wrap;
    background: {theme["small_bg"]};
    border: 1px solid {theme["border"]};
    border-radius: 14px;
    padding: 10px 18px;
    margin-bottom: 16px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}}
.pipeline-item {{
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 12px;
    color: {theme["muted"]};
    font-weight: 500;
}}
.status-dot {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    flex-shrink: 0;
}}
.dot-live    {{ background: #4ade80; box-shadow: 0 0 6px rgba(74,222,128,0.6); }}
.dot-stale   {{ background: #fbbf24; box-shadow: 0 0 6px rgba(251,191,36,0.6); }}
.dot-offline {{ background: #f87171; box-shadow: 0 0 6px rgba(248,113,113,0.6); }}
.pipeline-divider {{
    width: 1px;
    height: 16px;
    background: {theme["border"]};
}}
.export-row {{
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px solid {theme["border"]};
}}
.export-label {{
    font-size: 11px;
    font-weight: 600;
    color: {theme["soft_text"]};
    text-transform: uppercase;
    letter-spacing: 0.08em;
}}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
mode_icons = {"day": "☀️ Day", "sunset": "🌇 Sunset", "night": "🌙 Night"}
st.markdown(f"""
<div style='margin-bottom:12px;'>
    <div class='dash-title'>UAE Real-Time Weather</div>
    <div class='dash-subtitle'>Big Data Analytics Platform</div>
    <div class='dash-mode-badge'>{mode_icons[theme_mode]} Mode</div>
</div>
""", unsafe_allow_html=True)

# ================= PIPELINE STATUS BAR =================
def get_pipeline_status(data_file="weather_data.csv"):
    if not os.path.exists(data_file):
        return {"status": "offline", "dot": "dot-offline", "label": "Offline", "age": "—", "rpm": "—", "total": "—"}
    try:
        _df = pd.read_csv(data_file, on_bad_lines="skip")
        if _df.empty:
            return {"status": "offline", "dot": "dot-offline", "label": "No data", "age": "—", "rpm": "—", "total": str(0)}
        if "timestamp" in _df.columns:
            _df["timestamp"] = pd.to_datetime(_df["timestamp"], errors="coerce")
            last_ts = _df["timestamp"].max()
            if pd.isna(last_ts):
                age_sec = 999
            else:
                age_sec = int((datetime.now() - last_ts).total_seconds())
            cutoff = datetime.now() - timedelta(minutes=1)
            rpm = len(_df[_df["timestamp"] >= cutoff])
        else:
            age_sec, rpm = 999, 0
        if age_sec < 15:
            dot, label = "dot-live", "Live"
        elif age_sec < 60:
            dot, label = "dot-stale", "Delayed"
        else:
            dot, label = "dot-offline", "Stale"
        if age_sec < 60:
            age_str = f"{age_sec}s ago"
        elif age_sec < 3600:
            age_str = f"{age_sec // 60}m ago"
        else:
            age_str = f"{age_sec // 3600}h ago"
        return {"status": label.lower(), "dot": dot, "label": label,
                "age": age_str, "rpm": str(rpm), "total": str(len(_df))}
    except Exception:
        return {"status": "offline", "dot": "dot-offline", "label": "Error", "age": "—", "rpm": "—", "total": "—"}

ps = get_pipeline_status()
st.markdown(f"""
<div class='pipeline-bar'>
    <div class='pipeline-item'>
        <div class='status-dot {ps["dot"]}'></div>
        <span style='color:{"#4ade80" if ps["label"]=="Live" else "#fbbf24" if ps["label"]=="Delayed" else "#f87171"};
                     font-weight:600;'>{ps["label"]}</span>
    </div>
    <div class='pipeline-divider'></div>
    <div class='pipeline-item'>
        <span style='color:{theme["soft_text"]};'>Kafka →</span>
        <span>weather-topic</span>
    </div>
    <div class='pipeline-divider'></div>
    <div class='pipeline-item'>
        <span style='color:{theme["soft_text"]};'>Last update</span>
        <span>{ps["age"]}</span>
    </div>
    <div class='pipeline-divider'></div>
    <div class='pipeline-item'>
        <span style='color:{theme["soft_text"]};'>Rec/min</span>
        <span>{ps["rpm"]}</span>
    </div>
    <div class='pipeline-divider'></div>
    <div class='pipeline-item'>
        <span style='color:{theme["soft_text"]};'>Total records</span>
        <span>{ps["total"]}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= CITY SELECTOR =================
city_options = ["Ajman", "Dubai", "Sharjah", "Abu Dhabi", "Umm Al Quwain", "Fujairah", "Ras Al Khaimah"]

# FIX: Use session state instead of file to store selected city (works cross-machine)
if "selected_city" not in st.session_state:
    st.session_state.selected_city = "Ajman"

selected_city = st.selectbox(
    "Select Emirate",
    city_options,
    index=city_options.index(st.session_state.selected_city)
)
st.session_state.selected_city = selected_city

# ================= MAIN CONTENT =================
def render_dashboard():
    """Render the weather dashboard without infinite loops"""

    # Check if data file exists
    if not os.path.exists("weather_data.csv"):
        st.warning("⚠️ weather_data.csv not found. Run producer and processor first.")
        return

    try:
        df = pd.read_csv("weather_data.csv", on_bad_lines="skip")
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        return

    if df.empty:
        st.warning("weather_data.csv exists but is empty.")
        return

    # Parse timestamp if it exists
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        x_col = "timestamp"
    else:
        x_col = None

    # Filter by city
    if "city" in df.columns:
        df["city"] = df["city"].astype(str).str.replace("`", "", regex=False).str.strip()
        city_df = df[df["city"] == selected_city].copy()
    else:
        city_df = pd.DataFrame()

    if city_df.empty:
        st.markdown(f"""
        <div class='glass-card'>
            <div class='metric-label'>Selected City</div>
            <div class='metric-mid'>📍 {selected_city}</div>
            <hr class='divider'>
            <div style='color:{theme["muted"]}; font-size:14px;'>
                No records yet — waiting for producer and processor...
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    latest = city_df.iloc[-1]

    temp_c         = latest.get("temp_c", float("nan"))
    condition      = latest.get("condition", "-")
    humidity       = latest.get("humidity", float("nan"))
    wind_kph       = latest.get("wind_kph", float("nan"))
    uv             = latest.get("uv", float("nan"))
    pressure       = latest.get("pressure_mb", float("nan"))
    trend          = latest.get("trend", "-")
    feelslike      = latest.get("feelslike_c", "-")
    temp_category  = latest.get("temp_category", "-")
    humidity_level = latest.get("humidity_level", "-")
    wind_level     = latest.get("wind_level", "-")
    cloud_level    = latest.get("cloud_level", "-")
    alerts         = str(latest.get("alerts", "No alert"))

    humidity_note = interpret_humidity(humidity)
    uv_note       = interpret_uv(uv)
    wind_note     = interpret_wind(wind_kph)
    pressure_note = interpret_pressure(pressure)
    weather_icon  = get_weather_icon(condition, theme_mode)

    # ===== HERO ROW =====
    left, right = st.columns([1.3, 1])

    with left:
        st.markdown(f"""
        <div class='hero-card'>
            <div class='city-badge'>📍 {selected_city}</div>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <div style='font-size:64px; font-weight:200; color:#ffffff;
                                line-height:1; letter-spacing:-2px;'>{temp_c}°</div>
                    <div class='weather-condition'>{condition}</div>
                    <div style='margin-top:8px; color:{theme["soft_text"]}; font-size:13px;'>
                        Feels like {feelslike}°C
                    </div>
                    <div style='margin-top:14px;'>
                        <span class='info-pill'>↗ {trend}</span>
                        <span class='info-pill'>{temp_category}</span>
                        <span class='info-pill'>{humidity_level} humidity</span>
                        <span class='info-pill'>{wind_level} wind</span>
                    </div>
                </div>
                <div style='font-size:86px; opacity:0.88;'>{weather_icon}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        r1, r2 = st.columns(2)
        r3, r4 = st.columns(2)

        with r1:
            st.markdown(f"""
            <div class='small-card'>
                <div class='metric-label'>Humidity</div>
                <div class='metric-mid'>{humidity}%</div>
                <div class='metric-note'>{humidity_note}</div>
            </div>""", unsafe_allow_html=True)
        with r2:
            st.markdown(f"""
            <div class='small-card'>
                <div class='metric-label'>UV Index</div>
                <div class='metric-mid'>{uv}</div>
                <div class='metric-note'>{uv_note}</div>
            </div>""", unsafe_allow_html=True)
        with r3:
            st.markdown(f"""
            <div class='small-card'>
                <div class='metric-label'>Wind Speed</div>
                <div class='metric-mid'>{wind_kph} km/h</div>
                <div class='metric-note'>{wind_note}</div>
            </div>""", unsafe_allow_html=True)
        with r4:
            st.markdown(f"""
            <div class='small-card'>
                <div class='metric-label'>Pressure</div>
                <div class='metric-mid'>{pressure} mb</div>
                <div class='metric-note'>{pressure_note}</div>
            </div>""", unsafe_allow_html=True)

    st.write("")

    # ===== ANALYTICS STRIP =====
    st.markdown("<div class='section-title'>Analytics Overview</div>", unsafe_allow_html=True)
    a1, a2, a3, a4, a5 = st.columns(5)
    a1.metric("Record No",       latest.get("record_no", "-"))
    a2.metric("Temp Change °C",  latest.get("temp_change", "-"))
    a3.metric("Avg Temp °C",     latest.get("avg_temp", "-"))
    a4.metric("Max Temp °C",     latest.get("max_temp", "-"))
    a5.metric("Min Temp °C",     latest.get("min_temp", "-"))

    # ===== CHARTS =====
    st.markdown("<div class='section-title'>Visual Analytics</div>", unsafe_allow_html=True)

    metric_options = {
        "Humidity (%)":    "humidity",
        "Wind Speed (km/h)": "wind_kph",
        "Pressure (mb)":   "pressure_mb",
        "UV Index":        "uv",
        "Cloud (%)":       "cloud",
    }

    selected_metric_label = st.selectbox(
        "Metric to visualize",
        list(metric_options.keys()),
        key="metric_selector"
    )
    selected_metric = metric_options[selected_metric_label]

    chart1, chart2 = st.columns(2)

    with chart1:
        st.markdown("<div style='color:rgba(255,255,255,0.55); font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:4px;'>Temperature Performance</div>", unsafe_allow_html=True)
        if len(city_df) > 1:
            tf = go.Figure()
            tf.add_trace(go.Scatter(
                x=city_df[x_col] if x_col else city_df.index,
                y=city_df["temp_c"],
                mode="lines", name="Temperature (°C)",
                line=dict(color="#93c5fd", width=2.5, shape="spline"),
                fill="tozeroy", fillcolor="rgba(147,197,253,0.07)",
                hovertemplate="Time: %{x}<br>Temp: %{y}°C<extra></extra>"
            ))
            tf.add_trace(go.Scatter(
                x=city_df[x_col] if x_col else city_df.index,
                y=city_df["feelslike_c"],
                mode="lines", name="Feels Like (°C)",
                line=dict(color="#c4b5fd", width=1.5, dash="dot", shape="spline"),
                hovertemplate="Time: %{x}<br>Feels Like: %{y}°C<extra></extra>"
            ))
            tf = apply_chart_style(tf, f"{selected_city} — Temperature vs Feels Like", "", "°C")
            st.plotly_chart(tf, use_container_width=True)
        else:
            st.info("Not enough data yet.")

    with chart2:
        st.markdown(f"<div style='color:rgba(255,255,255,0.55); font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:4px;'>{selected_metric_label}</div>", unsafe_allow_html=True)
        if len(city_df) > 1:
            mf = go.Figure()
            mf.add_trace(go.Scatter(
                x=city_df[x_col] if x_col else city_df.index,
                y=city_df[selected_metric],
                mode="lines", name=selected_metric_label,
                line=dict(color="#6ee7b7", width=2.5, shape="spline"),
                fill="tozeroy", fillcolor="rgba(110,231,183,0.07)",
                hovertemplate=f"Time: %{{x}}<br>{selected_metric_label}: %{{y}}<extra></extra>"
            ))
            mf = apply_chart_style(mf, f"{selected_city} — {selected_metric_label}", "", selected_metric_label)
            mf.update_layout(showlegend=False)
            st.plotly_chart(mf, use_container_width=True)
        else:
            st.info("Not enough data yet.")

    # ===== CITY COMPARISON =====
    st.markdown("<div class='section-title'>City Comparison</div>", unsafe_allow_html=True)

    if "city" in df.columns:
        latest_by_city = df.groupby("city", as_index=False).tail(1).copy()
        if not latest_by_city.empty:
            c1, c2, c3 = st.columns(3)
            hottest_row = latest_by_city.loc[latest_by_city["temp_c"].astype(float).idxmax()]   if "temp_c"   in latest_by_city.columns else None
            humid_row   = latest_by_city.loc[latest_by_city["humidity"].astype(float).idxmax()] if "humidity" in latest_by_city.columns else None
            windy_row   = latest_by_city.loc[latest_by_city["wind_kph"].astype(float).idxmax()] if "wind_kph" in latest_by_city.columns else None

            with c1:
                if hottest_row is not None:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div class='metric-label'>Hottest City</div>
                        <div class='metric-mid'>{hottest_row['city']}</div>
                        <div class='metric-note'>{hottest_row['temp_c']}°C</div>
                    </div>""", unsafe_allow_html=True)
            with c2:
                if humid_row is not None:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div class='metric-label'>Highest Humidity</div>
                        <div class='metric-mid'>{humid_row['city']}</div>
                        <div class='metric-note'>{humid_row['humidity']}%</div>
                    </div>""", unsafe_allow_html=True)
            with c3:
                if windy_row is not None:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div class='metric-label'>Strongest Wind</div>
                        <div class='metric-mid'>{windy_row['city']}</div>
                        <div class='metric-note'>{windy_row['wind_kph']} km/h</div>
                    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # ===== REAL-TIME INSIGHTS =====
    st.markdown("<div class='section-title'>Real-Time Insights</div>", unsafe_allow_html=True)

    insights = []
    if pd.notna(temp_c):
        if temp_c >= 35:    insights.append(("🔥", "Temperature is elevated — extreme heat conditions."))
        elif temp_c <= 18:  insights.append(("❄️", "Temperature is relatively cool for the UAE."))
        else:               insights.append(("🌡️", "Temperature is within a comfortable range."))

    if pd.notna(humidity):
        if humidity > 60:   insights.append(("💧", "Humidity is elevated — comfort levels may be reduced."))
        elif humidity < 30: insights.append(("🌵", "Air is dry — low humidity conditions."))

    if pd.notna(wind_kph):
        if wind_kph >= 30:  insights.append(("💨", "Wind speed is strong and noticeable outdoors."))
        elif wind_kph < 10: insights.append(("🍃", "Calm wind conditions."))

    if pd.notna(uv):
        if uv >= 8:         insights.append(("☀️", "Very high UV — sun protection strongly recommended."))
        elif uv >= 3:       insights.append(("🕶️", "Moderate UV exposure — consider sunscreen."))

    if trend == "Stable":       insights.append(("📊", "Weather readings are stable over recent records."))
    elif trend == "Increasing": insights.append(("📈", "Readings show an upward trend."))
    elif trend == "Decreasing": insights.append(("📉", "Readings show a downward trend."))

    if condition == latest.get("most_common_condition", None):
        insights.append(("☁️", f"{condition} is the dominant condition recorded so far."))

    if not insights:
        insights.append(("✅", "All weather parameters are within normal range."))

    insights_html = "".join([
        f"<div class='insight-row'><span style='font-size:16px;'>{icon}</span><span>{text}</span></div>"
        for icon, text in insights
    ])
    st.markdown(f"<div class='glass-card'>{insights_html}</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # ===== UAE MAP =====
    st.markdown("<div class='section-title'>UAE Weather Map</div>", unsafe_allow_html=True)

    if "city" in df.columns and not df.empty:
        map_df = df.groupby("city", as_index=False).tail(1).copy()
        map_df["lat"] = map_df["city"].map(lambda x: city_coordinates.get(x, {}).get("lat"))
        map_df["lon"] = map_df["city"].map(lambda x: city_coordinates.get(x, {}).get("lon"))
        map_df = map_df.dropna(subset=["lat", "lon"])

        if not map_df.empty and "temp_c" in map_df.columns:
            map_fig = go.Figure()
            map_fig.add_trace(go.Scattermapbox(
                lat=map_df["lat"], lon=map_df["lon"],
                mode="markers+text",
                text=map_df["city"],
                textposition="top center",
                marker=dict(
                    size=16,
                    color=map_df["temp_c"],
                    colorscale="Blues",
                    showscale=True,
                    colorbar=dict(
                        title=dict(text="°C", font=dict(color="rgba(255,255,255,0.65)")),
                        tickfont=dict(color="rgba(255,255,255,0.65)")
                    )
                ),
                customdata=map_df[["temp_c", "humidity", "wind_kph", "condition"]],
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Temperature: %{customdata[0]}°C<br>"
                    "Humidity: %{customdata[1]}%<br>"
                    "Wind: %{customdata[2]} km/h<br>"
                    "Condition: %{customdata[3]}<extra></extra>"
                )
            ))
            map_fig.update_layout(
                mapbox_style="carto-darkmatter",
                mapbox=dict(center=dict(lat=24.8, lon=55.5), zoom=5.7),
                margin=dict(l=0, r=0, t=0, b=0),
                height=450,
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="rgba(255,255,255,0.70)")
            )
            st.plotly_chart(map_fig, use_container_width=True)

    # ===== BOTTOM ROW =====
    s1, s2, s3 = st.columns(3)

    alert_html = (
        f"<div class='no-alert-badge'>✓ {alerts}</div>"
        if alerts.lower() == "no alert"
        else f"<div class='alert-badge'>⚠ {alerts}</div>"
    )

    with s1:
        st.markdown(f"""
        <div class='glass-card'>
            <div class='metric-label'>Derived Categories</div>
            <div class='metric-mid'>{temp_category}</div>
            <div class='metric-note'>Temperature</div>
            <hr class='divider'>
            <div class='metric-mid'>{cloud_level}</div>
            <div class='metric-note'>Cloud cover</div>
        </div>""", unsafe_allow_html=True)

    with s2:
        st.markdown(f"""
        <div class='glass-card'>
            <div class='metric-label'>Condition Tracking</div>
            <div class='metric-mid'>{latest.get("most_common_condition", "-")}</div>
            <div class='metric-note'>Most common condition</div>
            <hr class='divider'>
            <div class='metric-mid'>{latest.get("condition_count", "-")}</div>
            <div class='metric-note'>Occurrences recorded</div>
        </div>""", unsafe_allow_html=True)

    with s3:
        st.markdown(f"""
        <div class='glass-card'>
            <div class='metric-label'>Alert Status</div>
            <div style='margin-top:10px;'>{alert_html}</div>
        </div>""", unsafe_allow_html=True)

    # ===== EXPORT ROW =====
    st.markdown("<div class='export-label' style='margin-top:22px; margin-bottom:8px;'>Export Data</div>", unsafe_allow_html=True)

    ex1, ex2, ex3 = st.columns(3)

    with ex1:
        csv_all = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Download All Cities — CSV",
            data=csv_all,
            file_name="uae_weather_all.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with ex2:
        csv_city = city_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"⬇ Download {selected_city} — CSV",
            data=csv_city,
            file_name=f"weather_{selected_city.lower().replace(' ', '_')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with ex3:
        latest_ts = city_df["timestamp"].max() if "timestamp" in city_df.columns else "N/A"
        report_lines = [
            "UAE REAL-TIME WEATHER ANALYTICS — SESSION REPORT",
            "=" * 52,
            f"Generated   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"City        : {selected_city}",
            f"Last update : {latest_ts}",
            f"Records     : {len(city_df)}",
            "",
            "LATEST READINGS",
            "-" * 30,
            f"Temperature : {temp_c} °C  (feels like {feelslike} °C)",
            f"Condition   : {condition}",
            f"Humidity    : {humidity}%  — {interpret_humidity(humidity)}",
            f"Wind        : {wind_kph} km/h  — {interpret_wind(wind_kph)}",
            f"Pressure    : {pressure} mb  — {interpret_pressure(pressure)}",
            f"UV Index    : {uv}  — {interpret_uv(uv)}",
            f"Cloud cover : {cloud_level}",
            "",
            "ANALYTICS SUMMARY",
            "-" * 30,
            f"Avg temp    : {latest.get('avg_temp', '-')} °C",
            f"Max temp    : {latest.get('max_temp', '-')} °C",
            f"Min temp    : {latest.get('min_temp', '-')} °C",
            f"Trend       : {trend}",
            f"Top condition: {latest.get('most_common_condition', '-')}",
            f"Alert       : {alerts}",
            "",
            "CITY COMPARISON (latest snapshot)",
            "-" * 30,
        ]
        if "city" in df.columns:
            snapshot = df.groupby("city", as_index=False).tail(1)
            for _, row in snapshot.iterrows():
                report_lines.append(
                    f"  {row.get('city','?'):<18} {row.get('temp_c','?')}°C   "
                    f"Humidity {row.get('humidity','?')}%   Wind {row.get('wind_kph','?')} km/h"
                )
        report_lines += ["", "=" * 52, "Platform: UAE Real-Time Weather Analytics", "Built with Apache Kafka · Python · Streamlit · Plotly"]
        report_text = "\n".join(report_lines).encode("utf-8")
        st.download_button(
            label="⬇ Download Summary Report — TXT",
            data=report_text,
            file_name=f"weather_report_{selected_city.lower().replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ================= RENDER ONCE =================
# Instead of infinite loop, render once and add a refresh button
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("Refresh Data", use_container_width=True):
        st.rerun()

with col2:
    auto_refresh = st.checkbox("Auto-refresh (5s)", value=False)

if auto_refresh:
    # Use time.sleep with st.rerun for auto-refresh, but don't use while True
    time.sleep(5)
    st.rerun()

# Render dashboard
render_dashboard()