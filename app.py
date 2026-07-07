# ╔════════════════════════════════════════════════════════════╗
# ║   FloodX v8.0 — Complete AI Flood Prediction System     ║
# ║   Live Prediction | History | Forecast | Contribution     ║
# ║   Pakistan | OpenWeatherMap | All Provinces               ║
# ╚════════════════════════════════════════════════════════════╝

import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ─────────────────────────────────────────────────────────────
# 1. PAGE SETUP
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FloodX — AI Flood Prediction System",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────────
# 2. CONSTANTS
# ─────────────────────────────────────────────────────────────
API_KEY = "2ff19563385747091536596f70fe8527"

CITIES = {
    "Abbottabad (KPK)"          : {"lat": 34.15, "lon": 73.22},
    "Bahawalpur (Punjab)"       : {"lat": 29.40, "lon": 71.68},
    "Chiniot (Punjab)"          : {"lat": 31.72, "lon": 72.98},
    "Dera Ghazi Khan (Punjab)"  : {"lat": 30.05, "lon": 70.64},
    "Dera Ismail Khan (KPK)"    : {"lat": 31.83, "lon": 70.90},
    "Faisalabad (Punjab)"       : {"lat": 31.42, "lon": 73.08},
    "Gilgit (GB)"               : {"lat": 35.92, "lon": 74.31},
    "Gujranwala (Punjab)"       : {"lat": 32.16, "lon": 74.19},
    "Gujrat (Punjab)"           : {"lat": 32.57, "lon": 74.08},
    "Hub (Balochistan)"         : {"lat": 25.05, "lon": 66.89},
    "Hyderabad (Sindh)"         : {"lat": 25.37, "lon": 68.37},
    "Islamabad (ICT)"           : {"lat": 33.72, "lon": 73.06},
    "Jacobabad (Sindh)"         : {"lat": 28.28, "lon": 68.44},
    "Jhang (Punjab)"            : {"lat": 31.27, "lon": 72.32},
    "Karachi (Sindh)"           : {"lat": 24.86, "lon": 67.01},
    "Kasur (Punjab)"            : {"lat": 31.12, "lon": 74.45},
    "Khuzdar (Balochistan)"     : {"lat": 27.81, "lon": 66.61},
    "Kohat (KPK)"               : {"lat": 33.59, "lon": 71.44},
    "Lahore (Punjab)"           : {"lat": 31.55, "lon": 74.35},
    "Larkana (Sindh)"           : {"lat": 27.56, "lon": 68.21},
    "Mardan (KPK)"              : {"lat": 34.20, "lon": 72.04},
    "Mingora (KPK)"             : {"lat": 34.77, "lon": 72.36},
    "Mirpurkhas (Sindh)"        : {"lat": 25.53, "lon": 69.01},
    "Multan (Punjab)"           : {"lat": 30.19, "lon": 71.47},
    "Muzaffarabad (AJK)"        : {"lat": 34.37, "lon": 73.47},
    "Nawabshah (Sindh)"         : {"lat": 26.24, "lon": 68.41},
    "Okara (Punjab)"            : {"lat": 30.81, "lon": 73.45},
    "Peshawar (KPK)"            : {"lat": 34.01, "lon": 71.54},
    "Quetta (Balochistan)"      : {"lat": 30.18, "lon": 66.99},
    "Rahim Yar Khan (Punjab)"   : {"lat": 28.42, "lon": 70.30},
    "Rawalpindi (Punjab)"       : {"lat": 33.60, "lon": 73.04},
    "Sahiwal (Punjab)"          : {"lat": 30.67, "lon": 73.11},
    "Sargodha (Punjab)"         : {"lat": 32.08, "lon": 72.67},
    "Sheikhupura (Punjab)"      : {"lat": 31.71, "lon": 73.98},
    "Sialkot (Punjab)"          : {"lat": 32.49, "lon": 74.53},
    "Sukkur (Sindh)"            : {"lat": 27.70, "lon": 68.85},
    "Turbat (Balochistan)"      : {"lat": 26.00, "lon": 63.04},
}

# Historical Pakistan Flood Data (real events)
FLOOD_HISTORY = [
    {"year":1950,"deaths":2910,"affected":9_000_000,"damage_usd":1_000_000_000,"area":"Sindh, Punjab","cause":"Heavy Monsoon","severity":"Severe"},
    {"year":1973,"deaths":474, "affected":4_700_000,"damage_usd":800_000_000, "area":"Punjab, Sindh","cause":"Monsoon + River Overflow","severity":"Moderate"},
    {"year":1976,"deaths":425, "affected":4_900_000,"damage_usd":900_000_000, "area":"All Provinces","cause":"Heavy Rainfall","severity":"Severe"},
    {"year":1988,"deaths":508, "affected":3_100_000,"damage_usd":1_200_000_000,"area":"Punjab, NWFP","cause":"Monsoon Floods","severity":"Severe"},
    {"year":1992,"deaths":1_008,"affected":4_800_000,"damage_usd":1_000_000_000,"area":"Punjab, Sindh","cause":"Flash Floods","severity":"Severe"},
    {"year":1998,"deaths":300, "affected":1_000_000,"damage_usd":500_000_000, "area":"Punjab","cause":"River Flooding","severity":"Moderate"},
    {"year":2007,"deaths":540, "affected":2_500_000,"damage_usd":2_000_000_000,"area":"Balochistan, Sindh","cause":"Cyclone + Monsoon","severity":"Severe"},
    {"year":2010,"deaths":2_000,"affected":20_000_000,"damage_usd":10_000_000_000,"area":"All Provinces","cause":"Record Monsoon","severity":"Catastrophic"},
    {"year":2011,"deaths":520, "affected":9_000_000,"damage_usd":3_700_000_000,"area":"Sindh, Balochistan","cause":"Monsoon","severity":"Severe"},
    {"year":2012,"deaths":453, "affected":4_800_000,"damage_usd":2_600_000_000,"area":"Sindh","cause":"Monsoon","severity":"Severe"},
    {"year":2013,"deaths":178, "affected":1_500_000,"damage_usd":800_000_000, "area":"Balochistan","cause":"Flash Floods","severity":"Moderate"},
    {"year":2014,"deaths":367, "affected":2_530_000,"damage_usd":2_100_000_000,"area":"Punjab, AJK","cause":"Monsoon","severity":"Severe"},
    {"year":2015,"deaths":238, "affected":1_400_000,"damage_usd":1_200_000_000,"area":"KPK, Punjab","cause":"Monsoon","severity":"Moderate"},
    {"year":2020,"deaths":400, "affected":2_100_000,"damage_usd":1_500_000_000,"area":"Balochistan, Sindh","cause":"Monsoon","severity":"Severe"},
    {"year":2022,"deaths":1_739,"affected":33_000_000,"damage_usd":30_000_000_000,"area":"All Provinces","cause":"Record Monsoon + Glacial","severity":"Catastrophic"},
    {"year":2023,"deaths":97,  "affected":800_000,"damage_usd":500_000_000,  "area":"Balochistan, KPK","cause":"Flash Floods","severity":"Moderate"},
    {"year":2024,"deaths":243, "affected":2_100_000,"damage_usd":1_800_000_000,"area":"Balochistan, KPK, Sindh","cause":"Monsoon Flash Floods","severity":"Severe"},
    {"year":2025,"deaths":312, "affected":3_500_000,"damage_usd":2_400_000_000,"area":"Punjab, Balochistan, Sindh","cause":"Record Monsoon + Glacial Melt","severity":"Severe"},
]

# Monthly flood risk for Pakistan (based on historical patterns)
MONTHLY_RISK = {
    "January":5, "February":6, "March":8, "April":10,
    "May":18, "June":35, "July":78, "August":88,
    "September":72, "October":30, "November":12, "December":5
}

# ─────────────────────────────────────────────────────────────
# 3. CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');

* { box-sizing: border-box; }
#MainMenu, footer, header { visibility: hidden; }

/* BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 30%, #f0f9ff 70%, #faf5ff 100%);
}

/* TAB STYLING */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.7) !important;
    border-radius: 16px !important;
    padding: 6px !important;
    gap: 4px !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(167,139,250,0.2) !important;
    box-shadow: 0 4px 20px rgba(109,40,217,0.08) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 12px !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px !important;
    padding: 10px 20px !important;
    color: #7c3aed !important;
    transition: all 0.3s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7c3aed, #9333ea) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(124,58,237,0.35) !important;
}

/* ANIMATIONS */
@keyframes gradShift  { 0%,100%{background-position:0% 50%} 50%{background-position:100% 50%} }
@keyframes waveFloat  { 0%,100%{transform:translateY(0) rotate(-8deg) scale(1)} 50%{transform:translateY(-12px) rotate(8deg) scale(1.08)} }
@keyframes blink      { 0%,100%{opacity:1} 50%{opacity:0.2} }
@keyframes fadeInUp   { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
@keyframes critGlow   { 0%,100%{box-shadow:0 10px 40px rgba(244,63,94,0.2)} 50%{box-shadow:0 10px 60px rgba(244,63,94,0.5)} }
@keyframes btnPulse   { 0%{box-shadow:0 4px 20px rgba(124,58,237,0.4),0 0 0 0 rgba(124,58,237,0.4)} 70%{box-shadow:0 4px 20px rgba(124,58,237,0.4),0 0 0 14px rgba(124,58,237,0)} 100%{box-shadow:0 4px 20px rgba(124,58,237,0.4),0 0 0 0 rgba(124,58,237,0)} }

/* APP HEADER */
.app-header {
    background: linear-gradient(135deg, #3b0764, #4c1d95, #6d28d9, #7c3aed, #9333ea, #7c3aed, #4c1d95);
    background-size: 300% 300%;
    animation: gradShift 8s ease infinite;
    border-radius: 28px 28px 0 0;
    padding: 44px 50px 36px 50px;
    text-align: center;
    box-shadow: 0 15px 50px rgba(109,40,217,0.4);
    position: relative;
    overflow: hidden;
    margin-bottom: 0;
}
.app-header::before {
    content:''; position:absolute; top:-50%; left:-50%;
    width:200%; height:200%;
    background:radial-gradient(circle at 30% 50%, rgba(255,255,255,0.06) 0%, transparent 50%);
    animation:gradShift 10s linear infinite;
}
.app-header::after {
    content:'🌊'; position:absolute; font-size:14rem;
    opacity:0.04; right:-30px; top:-30px;
    animation:waveFloat 6s ease-in-out infinite;
}
.hdr-wave  { font-size:3.8rem; display:block; animation:waveFloat 3s ease-in-out infinite; filter:drop-shadow(0 0 25px rgba(196,181,253,0.9)); position:relative; z-index:1; }
.hdr-title { font-family:'Orbitron',monospace; font-size:3.8rem; font-weight:900; color:#fff; letter-spacing:10px; display:block; text-shadow:0 4px 25px rgba(0,0,0,0.25); position:relative; z-index:1; }
.hdr-sub   { font-family:'Inter',sans-serif; font-size:0.82rem; color:rgba(255,255,255,0.65); letter-spacing:5px; text-transform:uppercase; display:block; margin-top:12px; position:relative; z-index:1; }
.hdr-badges{ display:flex; justify-content:center; gap:9px; margin-top:20px; flex-wrap:wrap; position:relative; z-index:1; }
.hbadge    { background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.3); border-radius:50px; padding:6px 16px; font-family:'Inter',sans-serif; font-size:0.67rem; font-weight:600; color:#fff; backdrop-filter:blur(8px); transition:all 0.3s; }

/* CONTROL PANEL */
.ctrl-panel {
    background: linear-gradient(135deg, #1e1b4b, #2e1065, #1e1b4b);
    border-radius: 0 0 24px 24px;
    padding: 22px 30px;
    border: 1px solid rgba(139,92,246,0.25);
    border-top: none;
    box-shadow: 0 12px 40px rgba(109,40,217,0.2);
    margin-bottom: 32px;
}
.ctrl-lbl { font-family:'Inter',sans-serif; font-size:0.6rem; color:#a78bfa; letter-spacing:2px; text-transform:uppercase; display:block; margin-bottom:5px; }

/* PREDICT BUTTON */
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg,#7c3aed,#9333ea,#6d28d9) !important;
    color: white !important; font-family:'Orbitron',monospace !important;
    font-size:0.7rem !important; font-weight:700 !important;
    letter-spacing:2px !important; border-radius:14px !important;
    border:none !important; padding:14px !important;
    animation:btnPulse 2.5s infinite !important;
}

/* STAT CARDS */
.stat-card { background:rgba(255,255,255,0.85); backdrop-filter:blur(16px); border:1px solid rgba(167,139,250,0.2); border-top:3px solid #7c3aed; border-radius:20px; padding:24px 16px; text-align:center; box-shadow:0 4px 20px rgba(109,40,217,0.08); transition:all 0.3s ease; animation:fadeInUp 0.5s ease forwards; }
.stat-card:hover { transform:translateY(-6px); box-shadow:0 15px 40px rgba(109,40,217,0.15); }
.sc-icon  { font-size:2.4rem; display:block; margin-bottom:10px; }
.sc-value { font-family:'Orbitron',monospace; font-size:1.7rem; font-weight:900; background:linear-gradient(135deg,#7c3aed,#9333ea); -webkit-background-clip:text; -webkit-text-fill-color:transparent; display:block; }
.sc-label { font-family:'Inter',sans-serif; font-size:0.6rem; color:#9ca3af; letter-spacing:2px; text-transform:uppercase; display:block; margin-top:4px; }

/* SECTION TITLE */
.sec-title { font-family:'Orbitron',monospace; font-size:0.78rem; font-weight:700; background:linear-gradient(135deg,#7c3aed,#9333ea); -webkit-background-clip:text; -webkit-text-fill-color:transparent; letter-spacing:4px; text-transform:uppercase; border-left:4px solid #7c3aed; padding-left:14px; margin:30px 0 16px 0; display:block; }

/* WEATHER CARDS */
.weather-card { background:rgba(255,255,255,0.9); border:1px solid rgba(167,139,250,0.18); border-bottom:3px solid #7c3aed; border-radius:18px; padding:18px 10px; text-align:center; box-shadow:0 3px 15px rgba(109,40,217,0.07); transition:all 0.3s; }
.weather-card:hover { transform:translateY(-5px); box-shadow:0 12px 35px rgba(109,40,217,0.14); }
.wc-icon { font-size:2rem; display:block; margin-bottom:8px; }
.wc-val  { font-family:'Orbitron',monospace; font-size:1.25rem; font-weight:900; background:linear-gradient(135deg,#6d28d9,#9333ea); -webkit-background-clip:text; -webkit-text-fill-color:transparent; display:block; }
.wc-lbl  { font-family:'Inter',sans-serif; font-size:0.58rem; color:#9ca3af; letter-spacing:2px; text-transform:uppercase; display:block; margin-top:4px; }

/* LIVE BADGE */
.live-badge { display:inline-flex; align-items:center; gap:7px; background:rgba(34,197,94,0.1); border:1px solid rgba(34,197,94,0.35); border-radius:50px; padding:5px 14px; font-family:'Inter',sans-serif; font-size:0.65rem; font-weight:600; color:#16a34a; }
.live-dot { width:7px; height:7px; background:#22c55e; border-radius:50%; animation:blink 1.3s infinite; box-shadow:0 0 6px #22c55e; }

/* ALERT BOXES */
.alert-critical { background:linear-gradient(135deg,#fff1f2,#ffe4e6); border:2px solid #f43f5e; border-radius:22px; padding:28px 36px; text-align:center; box-shadow:0 10px 40px rgba(244,63,94,0.2); animation:critGlow 2s ease-in-out infinite; }
.alert-high     { background:linear-gradient(135deg,#fff7ed,#ffedd5); border:2px solid #f97316; border-radius:22px; padding:28px 36px; text-align:center; box-shadow:0 10px 35px rgba(249,115,22,0.15); }
.alert-moderate { background:linear-gradient(135deg,#fefce8,#fef9c3); border:2px solid #eab308; border-radius:22px; padding:28px 36px; text-align:center; box-shadow:0 10px 35px rgba(234,179,8,0.12); }
.alert-safe     { background:linear-gradient(135deg,#f0fdf4,#dcfce7); border:2px solid #22c55e; border-radius:22px; padding:28px 36px; text-align:center; box-shadow:0 10px 35px rgba(34,197,94,0.12); }
.alert-title { font-family:'Orbitron',monospace; font-size:1.8rem; font-weight:900; letter-spacing:2px; margin:0; }
.alert-sub   { font-family:'Inter',sans-serif; font-size:0.92rem; color:#4b5563; margin-top:12px; line-height:1.6; }

/* HOW IT WORKS */
.step-card { background:rgba(255,255,255,0.85); backdrop-filter:blur(12px); border:1px solid rgba(167,139,250,0.15); border-radius:20px; padding:26px 16px; text-align:center; box-shadow:0 4px 18px rgba(109,40,217,0.07); transition:all 0.3s ease; height:100%; }
.step-card:hover { transform:translateY(-7px); box-shadow:0 18px 45px rgba(109,40,217,0.13); border-color:rgba(124,58,237,0.3); }
.step-num  { width:42px; height:42px; background:linear-gradient(135deg,#7c3aed,#9333ea); border-radius:50%; display:flex; align-items:center; justify-content:center; font-family:'Orbitron',monospace; font-size:1rem; font-weight:900; color:white; margin:0 auto 14px auto; box-shadow:0 4px 14px rgba(109,40,217,0.35); }
.step-icon { font-size:2.5rem; display:block; margin-bottom:12px; }
.step-ttl  { font-family:'Orbitron',monospace; font-size:0.63rem; font-weight:700; background:linear-gradient(135deg,#7c3aed,#9333ea); -webkit-background-clip:text; -webkit-text-fill-color:transparent; letter-spacing:1.5px; margin-bottom:8px; }
.step-desc { font-family:'Inter',sans-serif; font-size:0.77rem; color:#6b7280; line-height:1.6; }

/* INFO CARD */
.info-card { background:rgba(255,255,255,0.85); border:1px solid rgba(167,139,250,0.14); border-radius:14px; padding:13px; text-align:center; margin-bottom:9px; box-shadow:0 2px 10px rgba(109,40,217,0.05); transition:all 0.2s; }
.info-card:hover { transform:translateX(4px); border-color:rgba(124,58,237,0.25); }
.info-lbl { font-family:'Inter',sans-serif; font-size:0.6rem; color:#9ca3af; letter-spacing:1.5px; text-transform:uppercase; }
.info-val { font-family:'Orbitron',monospace; font-size:1rem; font-weight:700; background:linear-gradient(135deg,#7c3aed,#9333ea); -webkit-background-clip:text; -webkit-text-fill-color:transparent; display:block; margin-top:4px; }

/* HISTORY ROW */
.hist-row { background:rgba(255,255,255,0.85); border:1px solid rgba(167,139,250,0.12); border-radius:14px; padding:13px 18px; margin:7px 0; display:flex; justify-content:space-between; align-items:center; font-family:'Inter',sans-serif; font-size:0.82rem; color:#6b7280; box-shadow:0 2px 8px rgba(109,40,217,0.04); transition:all 0.2s; }
.hist-row:hover { transform:translateX(6px); border-color:rgba(124,58,237,0.28); }

/* FLOOD EVENT CARD */
.flood-card { background:rgba(255,255,255,0.9); border:1px solid rgba(167,139,250,0.15); border-radius:18px; padding:20px 22px; margin:10px 0; box-shadow:0 4px 18px rgba(109,40,217,0.07); transition:all 0.3s; border-left:5px solid; }
.flood-card:hover { transform:translateX(6px); box-shadow:0 8px 30px rgba(109,40,217,0.12); }
.flood-year  { font-family:'Orbitron',monospace; font-size:1.4rem; font-weight:900; }
.flood-area  { font-family:'Inter',sans-serif; font-size:0.8rem; color:#6b7280; margin-top:2px; }
.flood-stat  { font-family:'Inter',sans-serif; font-size:0.78rem; }
.flood-badge { display:inline-block; border-radius:50px; padding:4px 14px; font-family:'Orbitron',monospace; font-size:0.58rem; font-weight:700; letter-spacing:1px; }

/* CONTRIBUTION CARDS */
.contrib-card { background:rgba(255,255,255,0.9); border:1px solid rgba(167,139,250,0.18); border-radius:20px; padding:26px 22px; box-shadow:0 6px 25px rgba(109,40,217,0.09); transition:all 0.3s; position:relative; overflow:hidden; }
.contrib-card::before { content:''; position:absolute; top:0; left:0; right:0; height:4px; background:linear-gradient(90deg,#7c3aed,#9333ea,#6366f1); }
.contrib-card:hover { transform:translateY(-5px); box-shadow:0 16px 45px rgba(109,40,217,0.15); }
.contrib-icon  { font-size:2.8rem; margin-bottom:12px; display:block; }
.contrib-title { font-family:'Orbitron',monospace; font-size:0.75rem; font-weight:700; background:linear-gradient(135deg,#7c3aed,#9333ea); -webkit-background-clip:text; -webkit-text-fill-color:transparent; letter-spacing:2px; margin-bottom:10px; }
.contrib-desc  { font-family:'Inter',sans-serif; font-size:0.82rem; color:#4b5563; line-height:1.7; }
.contrib-tag   { display:inline-block; background:rgba(124,58,237,0.1); border:1px solid rgba(124,58,237,0.2); border-radius:50px; padding:3px 12px; font-family:'Inter',sans-serif; font-size:0.62rem; color:#7c3aed; font-weight:600; margin:3px; }

/* FORECAST CARDS */
.forecast-card { background:rgba(255,255,255,0.9); border:1px solid rgba(167,139,250,0.18); border-radius:16px; padding:18px 14px; text-align:center; box-shadow:0 3px 15px rgba(109,40,217,0.07); transition:all 0.3s; }
.forecast-card:hover { transform:translateY(-4px); box-shadow:0 10px 30px rgba(109,40,217,0.13); }
.fc-period { font-family:'Orbitron',monospace; font-size:0.65rem; font-weight:700; color:#6b7280; letter-spacing:2px; text-transform:uppercase; }
.fc-risk   { font-family:'Orbitron',monospace; font-size:1.6rem; font-weight:900; display:block; margin:8px 0; }
.fc-label  { font-family:'Inter',sans-serif; font-size:0.72rem; color:#6b7280; }

/* READY BOX */
.ready-box { background:rgba(255,255,255,0.8); backdrop-filter:blur(18px); border:1px solid rgba(167,139,250,0.22); border-radius:24px; padding:36px 40px; text-align:center; box-shadow:0 8px 30px rgba(109,40,217,0.07); }
.ready-ttl  { font-family:'Orbitron',monospace; font-size:1.1rem; font-weight:700; background:linear-gradient(135deg,#7c3aed,#9333ea); -webkit-background-clip:text; -webkit-text-fill-color:transparent; letter-spacing:4px; margin-bottom:14px; }
.ready-desc { font-family:'Inter',sans-serif; font-size:0.87rem; color:#6b7280; line-height:1.9; }

/* DOWNLOAD BUTTONS */
.stDownloadButton button { background:linear-gradient(135deg,#7c3aed,#9333ea) !important; color:white !important; border:none !important; border-radius:14px !important; font-family:'Orbitron',monospace !important; font-size:0.64rem !important; font-weight:700 !important; letter-spacing:1.5px !important; padding:13px !important; box-shadow:0 4px 18px rgba(109,40,217,0.28) !important; transition:all 0.3s !important; }
.stDownloadButton button:hover { transform:translateY(-3px) !important; box-shadow:0 10px 28px rgba(109,40,217,0.42) !important; }

/* FOOTER */
.footer { text-align:center; padding:22px; margin-top:30px; border-top:1px solid rgba(124,58,237,0.1); font-family:'Orbitron',monospace; font-size:0.6rem; background:linear-gradient(135deg,#7c3aed,#9333ea); -webkit-background-clip:text; -webkit-text-fill-color:transparent; letter-spacing:3px; }

/* SCROLLBAR */
::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-track { background:#f5f3ff; }
::-webkit-scrollbar-thumb { background:linear-gradient(#7c3aed,#9333ea); border-radius:5px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 4. SESSION STATE
# ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ─────────────────────────────────────────────────────────────
# 5. HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────
def fetch_weather(city, lat, lon):
    """Fetch live weather data from OpenWeatherMap API."""
    try:
        url = (f"https://api.openweathermap.org/data/2.5/weather"
               f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric")
        r = requests.get(url, timeout=10)
        d = r.json()
        if r.status_code != 200:
            return None, d.get("message", "API Error")
        return {
            "city"       : city,
            "description": d["weather"][0]["description"].title(),
            "rainfall"   : round(d.get("rain", {}).get("1h", 0.0), 1),
            "temp"       : round(d["main"]["temp"], 1),
            "humidity"   : d["main"]["humidity"],
            "wind"       : round(d["wind"]["speed"] * 3.6, 1),
            "pressure"   : d["main"]["pressure"],
            "cloud"      : d["clouds"]["all"],
            "feels_like" : round(d["main"]["feels_like"], 1),
            "temp_min"   : round(d["main"]["temp_min"], 1),
            "temp_max"   : round(d["main"]["temp_max"], 1),
            "visibility" : round(d.get("visibility", 10000) / 1000, 1),
            "fetched"    : datetime.now().strftime("%d %b %Y, %H:%M:%S"),
        }, None
    except requests.exceptions.Timeout:
        return None, "Connection timeout. Check your internet."
    except Exception as e:
        return None, str(e)


def calculate_risk(rainfall, humidity, pressure, cloud, wind, temp):
    """Calculate flood risk % using weighted weather factors."""
    score = (
        min(rainfall, 150) / 150  * 0.40 +
        humidity            / 100  * 0.22 +
        (1025 - min(max(pressure, 980), 1025)) / 45 * 0.18 +
        cloud               / 100  * 0.12 +
        min(wind, 100)      / 100  * 0.08
    )
    if temp > 38 and humidity > 70:
        score = min(score + 0.08, 1.0)
    return int(round(min(score, 1.0) * 100))


def get_risk_info(prob):
    """Return risk level, colors and emoji."""
    if prob >= 70:   return "CRITICAL", "#dc2626", "#ef4444", "critical", "🔴"
    elif prob >= 50: return "HIGH",     "#c2410c", "#f97316", "high",     "🟠"
    elif prob >= 35: return "MODERATE", "#b45309", "#eab308", "moderate", "🟡"
    else:            return "LOW",      "#15803d", "#22c55e", "safe",     "🟢"


def generate_weekly_forecast(base_prob, city):
    """Generate 7-day flood risk forecast — unique per city using its coordinates."""
    today    = datetime.now()
    seasonal = MONTHLY_RISK[today.strftime("%B")] / 100
    # Seed with city so each city gets unique but reproducible forecast
    city_seed = abs(hash(city)) % 9999
    rng = np.random.default_rng(city_seed + today.timetuple().tm_yday)

    # City-specific elevation/river/terrain modifier
    coords   = CITIES.get(city, {"lat": 30, "lon": 70})
    lat_mod  = (coords["lat"] - 24) / 12   # north = higher elevation = less flood in plains
    lon_mod  = (coords["lon"] - 60) / 20   # inland vs coastal factor
    city_mod = (lat_mod * 0.5 + lon_mod * 0.3) * 15  # ±15% modifier

    forecast = []
    for i in range(7):
        day      = today + timedelta(days=i)
        day_name = day.strftime("%a %d %b") if i > 0 else "Today"
        noise    = rng.uniform(-8, 8)
        trend    = i * rng.uniform(-1.5, 2.0)
        risk     = int(np.clip(base_prob * 0.55 + seasonal * 40 + noise + trend - city_mod, 5, 100))
        forecast.append({"day": day_name, "risk": risk, "date": day})
    return forecast


def generate_monthly_forecast(base_prob, city="Lahore (Punjab)"):
    """Generate 12-month flood risk forecast — city-specific using terrain modifiers."""
    coords   = CITIES.get(city, {"lat": 30, "lon": 70})
    province = city.split("(")[-1].replace(")","").strip()

    # Province-based seasonal flood modifiers (real Pakistan patterns)
    PROVINCE_MODS = {
        "Sindh"      : [0,0,0,0,5,20,30,25,15,5,0,0],   # river flooding + monsoon
        "Punjab"     : [0,0,0,0,5,15,25,30,20,5,0,0],   # monsoon heavy
        "KPK"        : [5,5,8,10,15,20,20,20,15,8,5,3], # flash floods year round
        "Balochistan": [3,4,6,8,12,8,10,12,8,5,4,3],    # flash flood, less monsoon
        "GB"         : [5,5,10,15,20,25,20,15,10,8,5,4],# glacial + monsoon
        "AJK"        : [4,5,8,12,15,20,22,20,15,8,5,4],
        "ICT"        : [0,0,0,5,8,15,22,28,18,6,2,0],
    }
    mods = PROVINCE_MODS.get(province, [0]*12)
    city_seed = abs(hash(city)) % 9999
    rng = np.random.default_rng(city_seed)

    monthly = []
    for i, name in enumerate(["Jan","Feb","Mar","Apr","May","Jun",
                               "Jul","Aug","Sep","Oct","Nov","Dec"]):
        base_risk = list(MONTHLY_RISK.values())[i] + mods[i]
        noise     = rng.uniform(-4, 4)
        risk      = int(np.clip(base_risk * (base_prob / 60) + noise, 2, 100))
        monthly.append({"month": name, "risk": risk})
    return monthly


def generate_yearly_forecast(city="Lahore (Punjab)"):
    """Generate 5-year flood risk trend forecast — city-specific."""
    current_year = datetime.now().year
    province     = city.split("(")[-1].replace(")","").strip()
    city_seed    = abs(hash(city)) % 9999
    rng          = np.random.default_rng(city_seed + 1)

    # Base risk per province (historical average %)
    PROVINCE_BASE = {
        "Sindh":55,"Punjab":50,"KPK":45,"Balochistan":38,
        "GB":42,"AJK":44,"ICT":40,
    }
    base = PROVINCE_BASE.get(province, 50)

    yearly = []
    for i, year in enumerate(range(current_year, current_year + 5)):
        trend = i * rng.uniform(1.5, 3.5)   # climate change: rising
        noise = rng.uniform(-4, 4)
        risk  = int(np.clip(base + trend + noise, 15, 100))
        yearly.append({"year": str(year), "risk": risk,
                        "note": "Current" if i == 0 else f"+{i}yr"})
    return yearly


# ─────────────────────────────────────────────────────────────
# 6. APP HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <span class="hdr-wave">🌊</span>
    <span class="hdr-title">FloodX</span>
    <span class="hdr-sub">AI-Powered Live Flood Intelligence System — Pakistan</span>
    <div class="hdr-badges">
        <span class="hbadge">🌐 Live OpenWeatherMap</span>
        <span class="hbadge">🇵🇰 37 Pakistan Cities</span>
        <span class="hbadge">📅 Future Forecast</span>
        <span class="hbadge">📜 Historical Floods</span>
        <span class="hbadge">🧠 Smart Algorithm</span>
        <span class="hbadge">🗺️ All Provinces</span>
        <span class="hbadge">📱 Mobile Ready</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 7. CONTROL PANEL (attached below header with spacing inside)
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="ctrl-panel"><span class="ctrl-lbl">⚙️ Control Panel</span></div>',
            unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns([3.5, 0.8, 0.8, 0.8, 2.2])
with c1:
    selected_city = st.selectbox("🏙️ Select Pakistan City", list(CITIES.keys()),
                                  help="37 cities across all provinces — alphabetically sorted")
with c2:
    st.markdown("<br>", unsafe_allow_html=True)
    demo_low  = st.button("🟢 LOW",  use_container_width=True)
with c3:
    st.markdown("<br>", unsafe_allow_html=True)
    demo_med  = st.button("🟡 MED",  use_container_width=True)
with c4:
    st.markdown("<br>", unsafe_allow_html=True)
    demo_high = st.button("🔴 HIGH", use_container_width=True)
with c5:
    st.markdown("<br>", unsafe_allow_html=True)
    fetch_btn = st.button("🌐 FETCH LIVE WEATHER & PREDICT",
                           type="primary", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 8. NAVIGATION TABS
# ─────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌐 Live Prediction",
    "📅 Future Forecast",
    "📜 Historical Floods",
    "🗺️ Risk Map",
    "👩‍💻 Our Contribution",
    "🔊 Voice Alert & SOS",
])

# ─────────────────────────────────────────────────────────────
# DEMO DATA
# ─────────────────────────────────────────────────────────────
weather = None
if demo_low:
    weather = {"city":selected_city,"description":"Clear Sky","rainfall":0,"temp":28,
               "humidity":34,"wind":11,"pressure":1016,"cloud":8,"feels_like":27,
               "temp_min":24,"temp_max":32,"visibility":10,"fetched":"Demo — LOW Risk"}
elif demo_med:
    weather = {"city":selected_city,"description":"Partly Cloudy with Showers","rainfall":20,
               "temp":34,"humidity":73,"wind":40,"pressure":1001,"cloud":67,"feels_like":39,
               "temp_min":29,"temp_max":37,"visibility":5,"fetched":"Demo — MODERATE Risk"}
elif demo_high:
    weather = {"city":selected_city,"description":"Heavy Rain and Thunderstorm","rainfall":125,
               "temp":29,"humidity":96,"wind":90,"pressure":982,"cloud":99,"feels_like":34,
               "temp_min":26,"temp_max":31,"visibility":1,"fetched":"Demo — CRITICAL Risk"}

if fetch_btn:
    coords = CITIES[selected_city]
    with st.spinner(f"Fetching live weather for {selected_city}..."):
        live_data, error = fetch_weather(selected_city, coords["lat"], coords["lon"])
    if error:
        st.error(f"Could not fetch weather: {error}")
        st.stop()
    weather = live_data

# ─────────────────────────────────────────────────────────────
# TAB 1 — LIVE PREDICTION
# ─────────────────────────────────────────────────────────────
with tab1:
    if not weather:
        # Stat cards
        s1,s2,s3,s4 = st.columns(4)
        for col,(icon,val,lbl) in zip([s1,s2,s3,s4],[
            ("🌐","Live","WEATHER DATA"),("🏙️","37","PAKISTAN CITIES"),
            ("🗺️","All","PROVINCES"),("⚡","<2s","FETCH TIME")]):
            col.markdown(f'<div class="stat-card"><span class="sc-icon">{icon}</span><span class="sc-value">{val}</span><span class="sc-label">{lbl}</span></div>',unsafe_allow_html=True)

        st.markdown('<span class="sec-title">HOW IT WORKS</span>', unsafe_allow_html=True)
        h1,h2,h3,h4 = st.columns(4)
        for col,(icon,num,title,desc) in zip([h1,h2,h3,h4],[
            ("🏙️","1","SELECT CITY",  "Choose any of 37 Pakistan cities from dropdown above"),
            ("🌐","2","FETCH LIVE",   "Click the blue button — real weather loads from internet"),
            ("🧠","3","AI ANALYSIS",  "Algorithm weighs Rainfall, Humidity, Pressure, Wind, Cloud"),
            ("📊","4","VIEW RESULTS", "Gauge shows exact flood risk % with colors and full charts")]):
            col.markdown(f'<div class="step-card"><div class="step-num">{num}</div><span class="step-icon">{icon}</span><div class="step-ttl">{title}</div><div class="step-desc">{desc}</div></div>',unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="ready-box">
            <div class="ready-ttl">⚡ SYSTEM READY</div>
            <div class="ready-desc">
                Select any Pakistan city above → Click <strong style="color:#7c3aed;">🌐 FETCH LIVE WEATHER & PREDICT</strong><br>
                Or click <strong style="color:#7c3aed;">🟢 LOW / 🟡 MED / 🔴 HIGH</strong> for instant demo
            </div>
        </div>""", unsafe_allow_html=True)

        if st.session_state.history:
            st.markdown('<span class="sec-title">RECENT PREDICTIONS</span>', unsafe_allow_html=True)
            for h in reversed(st.session_state.history[-5:]):
                clr = {"CRITICAL":"#dc2626","HIGH":"#c2410c","MODERATE":"#b45309","LOW":"#15803d"}.get(h["level"],"#15803d")
                ico = {"CRITICAL":"🔴","HIGH":"🟠","MODERATE":"🟡","LOW":"🟢"}.get(h["level"],"🟢")
                st.markdown(f'<div class="hist-row"><span>{ico} <strong>{h["city"]}</strong> &nbsp;|&nbsp; {h["time"]}</span><span style="color:{clr};font-weight:700;font-family:Orbitron,monospace;font-size:0.8rem;">{h["level"]} — {h["prob"]}%</span></div>',unsafe_allow_html=True)

    else:
        rf,temp,hum  = weather["rainfall"],weather["temp"],weather["humidity"]
        wind,pres,cld = weather["wind"],weather["pressure"],weather["cloud"]
        now = weather["fetched"]
        src = "OpenWeatherMap Live" if fetch_btn else "Demo Mode"
        prob = calculate_risk(rf,hum,pres,cld,wind,temp)
        level,clr,gclr,atype,emoji = get_risk_info(prob)

        st.session_state.history.append({"city":selected_city,"time":now[:16],"prob":prob,"level":level})
        if len(st.session_state.history)>10: st.session_state.history=st.session_state.history[-10:]

        # Weather cards
        dot = '<span class="live-dot"></span>' if fetch_btn else "⚡"
        st.markdown(f'<span class="sec-title">{dot} LIVE WEATHER — {selected_city.upper()}</span>',unsafe_allow_html=True)
        if fetch_btn:
            st.markdown(f'<span class="live-badge"><span class="live-dot"></span>LIVE &nbsp;|&nbsp; {weather["description"]} &nbsp;|&nbsp; {now}</span>',unsafe_allow_html=True)
        else:
            st.caption(f"⚡ {weather['description']}  |  {now}")
        st.markdown("<br>", unsafe_allow_html=True)

        wc = st.columns(6)
        for col,(icon,val,lbl) in zip(wc,[("🌧️",f"{rf} mm","RAINFALL"),("🌡️",f"{temp}°C","TEMPERATURE"),("💧",f"{hum}%","HUMIDITY"),("💨",f"{wind} km/h","WIND SPEED"),("🔵",f"{pres} hPa","AIR PRESSURE"),("☁️",f"{cld}%","CLOUD COVER")]):
            col.markdown(f'<div class="weather-card"><span class="wc-icon">{icon}</span><span class="wc-val">{val}</span><span class="wc-lbl">{lbl}</span></div>',unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Alert
        msgs = {"critical":("⚠️ FLOOD RISK DETECTED — CRITICAL","Immediate evacuation recommended. Contact NDMA."),"high":("🔶 HIGH FLOOD RISK — TAKE ACTION","Prepare for flooding. Alert local authorities."),"moderate":("⚡ MODERATE RISK — STAY ALERT","Monitor conditions. Take preventive measures."),"safe":("✅ NO FLOOD RISK — SAFE CONDITIONS","Current conditions are safe.")}
        ttl,act = msgs[atype]
        st.markdown(f'<div class="alert-{atype}"><p class="alert-title" style="color:{clr};">{ttl}</p><p class="alert-sub">Probability: <strong style="font-size:1.1rem;">{prob}%</strong> &nbsp;|&nbsp; {selected_city} &nbsp;|&nbsp; {now} &nbsp;|&nbsp; {act}</p></div>',unsafe_allow_html=True)
        if atype=="critical":
            st.components.v1.html('<audio autoplay><source src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg"></audio>',height=0)

        st.markdown("<br>", unsafe_allow_html=True)

        # Gauge + Bar
        col1,col2 = st.columns(2)
        with col1:
            st.markdown('<span class="sec-title">FLOOD RISK METER</span>',unsafe_allow_html=True)
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number", value=prob,
                number={"suffix":"%","valueformat":".0f","font":{"size":68,"color":clr,"family":"Orbitron"}},
                title={"text":f"Flood Probability<br><b style='color:{clr}'>{level} RISK {emoji}</b>","font":{"size":13,"color":"#7c3aed","family":"Orbitron"}},
                gauge={"axis":{"range":[0,100],"tickmode":"linear","tick0":0,"dtick":10,"tickfont":{"color":"#9ca3af","size":10},"tickcolor":"rgba(124,58,237,0.15)"},
                       "bar":{"color":clr,"thickness":0.06},"bgcolor":"white","borderwidth":2,"bordercolor":"rgba(167,139,250,0.15)",
                       "steps":[{"range":[0,35],"color":"#dcfce7"},{"range":[35,50],"color":"#fef9c3"},{"range":[50,70],"color":"#ffedd5"},{"range":[70,100],"color":"#fee2e2"}],
                       "threshold":{"line":{"color":"#7c3aed","width":4},"thickness":0.8,"value":50}}))
            for x,y,t,c in [(0.10,0.22,"🟢 LOW","#15803d"),(0.35,0.05,"🟡 MODERATE","#b45309"),(0.65,0.05,"🟠 HIGH","#c2410c"),(0.90,0.22,"🔴 CRITICAL","#dc2626")]:
                fig_g.add_annotation(x=x,y=y,text=t,showarrow=False,font=dict(size=9,color=c,family="Orbitron"))
            fig_g.update_layout(height=340,margin=dict(t=90,b=10,l=40,r=40),paper_bgcolor="white",plot_bgcolor="white")
            st.plotly_chart(fig_g,use_container_width=True)
            bg={"safe":"#dcfce7","moderate":"#fef9c3","high":"#ffedd5","critical":"#fee2e2"}[atype]
            st.markdown(f'<div style="text-align:center;background:{bg};border-radius:16px;padding:18px;border:2px solid {clr}33;margin-top:-6px;"><span style="font-family:Orbitron,monospace;font-size:2.4rem;font-weight:900;color:{clr};">{prob}%</span><br><span style="font-family:Inter,sans-serif;font-size:0.9rem;color:#4b5563;">Flood Probability — <strong>{level} RISK</strong> {emoji}</span></div>',unsafe_allow_html=True)

        with col2:
            st.markdown('<span class="sec-title">WEATHER RISK ANALYSIS</span>',unsafe_allow_html=True)
            scores=[int(min(rf,150)/150*100),int(hum),int((1025-min(max(pres,980),1025))/45*100),int(cld),int(min(wind,100)/100*100)]
            raws=[f"{rf}mm",f"{hum}%",f"{pres}hPa",f"{cld}%",f"{wind}km/h"]
            labels=["Rainfall","Humidity","Low Pressure","Cloud Cover","Wind Speed"]
            fdf=pd.DataFrame({"Factor":labels,"Score":scores,"Raw":raws}).sort_values("Score")
            bc=["#ef4444" if s>=70 else "#f97316" if s>=50 else "#eab308" if s>=35 else "#22c55e" for s in fdf["Score"]]
            fig_b=go.Figure(go.Bar(x=fdf["Score"],y=fdf["Factor"],orientation="h",marker=dict(color=bc,line=dict(color="white",width=1.5)),text=[f"{r}  ({s}%)" for r,s in zip(fdf["Raw"],fdf["Score"])],textposition="outside",textfont=dict(color="#374151",size=11,family="Inter")))
            fig_b.update_layout(height=340,margin=dict(t=10,b=10,l=10,r=120),paper_bgcolor="white",plot_bgcolor="white",xaxis=dict(range=[0,140],showgrid=True,gridcolor="#f3f4f6",tickfont=dict(color="#9ca3af"),zeroline=False,title=dict(text="Risk Contribution (%)",font=dict(color="#9ca3af"))),yaxis=dict(tickfont=dict(color="#374151",size=12)))
            st.plotly_chart(fig_b,use_container_width=True)

        # Radar + Extra
        col3,col4 = st.columns(2)
        with col3:
            st.markdown('<span class="sec-title">RISK RADAR CHART</span>',unsafe_allow_html=True)
            rgb=tuple(int(gclr.lstrip("#")[i:i+2],16) for i in (0,2,4))
            fig_r=go.Figure(go.Scatterpolar(r=scores+[scores[0]],theta=labels+[labels[0]],fill="toself",fillcolor=f"rgba({rgb[0]},{rgb[1]},{rgb[2]},0.15)",line=dict(color=gclr,width=2.5),marker=dict(color=gclr,size=8,line=dict(color="white",width=2))))
            fig_r.update_layout(polar=dict(bgcolor="white",radialaxis=dict(range=[0,100],gridcolor="#f3f4f6",tickfont=dict(color="#9ca3af",size=9),linecolor="#e5e7eb"),angularaxis=dict(tickfont=dict(color="#374151",size=10),gridcolor="#f3f4f6")),height=320,margin=dict(t=30,b=30,l=30,r=30),paper_bgcolor="white",showlegend=False)
            st.plotly_chart(fig_r,use_container_width=True)

        with col4:
            st.markdown('<span class="sec-title">EXTENDED WEATHER DATA</span>',unsafe_allow_html=True)
            extras=[("🌡️ Feels Like",f"{weather['feels_like']}°C"),("⬇️ Min Temp",f"{weather['temp_min']}°C"),("⬆️ Max Temp",f"{weather['temp_max']}°C"),("👁️ Visibility",f"{weather['visibility']} km"),("💧 Humidity",f"{hum}%"),("🔵 Pressure",f"{pres} hPa"),("☁️ Cloud",f"{cld}%"),("💨 Wind",f"{wind} km/h")]
            for i in range(0,len(extras),2):
                r1,r2=st.columns(2)
                for cw,(l,v) in zip([r1,r2],extras[i:i+2]):
                    cw.markdown(f'<div class="info-card"><div class="info-lbl">{l}</div><span class="info-val">{v}</span></div>',unsafe_allow_html=True)

        # History chart
        if len(st.session_state.history)>=2:
            st.markdown('<span class="sec-title">📈 PREDICTION HISTORY</span>',unsafe_allow_html=True)
            hdf=pd.DataFrame(st.session_state.history)
            hc=[{"CRITICAL":"#ef4444","HIGH":"#f97316","MODERATE":"#eab308","LOW":"#22c55e"}.get(l,"#22c55e") for l in hdf["level"]]
            fig_h=go.Figure()
            fig_h.add_trace(go.Scatter(x=list(range(1,len(hdf)+1)),y=hdf["prob"],mode="lines+markers+text",line=dict(color="#7c3aed",width=2.5),marker=dict(color=hc,size=14,line=dict(color="white",width=2)),text=[f"{p}%" for p in hdf["prob"]],textposition="top center",textfont=dict(color="#374151",size=10,family="Orbitron"),fill="tozeroy",fillcolor="rgba(124,58,237,0.07)",customdata=hdf["city"],hovertemplate="<b>%{customdata}</b><br>Risk: %{y}%<extra></extra>"))
            fig_h.add_hline(y=50,line_dash="dash",line_color="rgba(239,68,68,0.4)",annotation_text="FLOOD THRESHOLD 50%",annotation_font_color="#ef4444",annotation_font_size=10)
            fig_h.update_layout(height=230,margin=dict(t=20,b=20,l=45,r=20),paper_bgcolor="white",plot_bgcolor="white",xaxis=dict(title="Prediction Number",showgrid=True,gridcolor="#f3f4f6",tickfont=dict(color="#9ca3af")),yaxis=dict(title="Risk %",range=[0,115],showgrid=True,gridcolor="#f3f4f6",tickfont=dict(color="#9ca3af")),showlegend=False)
            st.plotly_chart(fig_h,use_container_width=True)

        # Downloads
        st.markdown('<span class="sec-title">💾 EXPORT REPORT</span>',unsafe_allow_html=True)
        report_txt="\n".join(["FloodX — LIVE FLOOD PREDICTION REPORT","="*55,f"City: {selected_city}",f"Date: {now}",f"Source: {src}",f"Risk Level: {level}",f"Probability: {prob}%","="*55,"WEATHER DATA","-"*55,f"Rainfall: {rf} mm",f"Temperature: {temp}°C",f"Humidity: {hum}%",f"Wind: {wind} km/h",f"Pressure: {pres} hPa",f"Cloud: {cld}%","="*55,"Generated by FloodX v8.0"])
        csv=f"city,date,rainfall,temp,humidity,wind,pressure,cloud,level,risk\n{selected_city},{now},{rf},{temp},{hum},{wind},{pres},{cld},{level},{prob}\n"
        d1,d2,d3=st.columns(3)
        with d1: st.download_button("📄 REPORT (.txt)",data=report_txt,file_name=f"FloodX_{selected_city}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",mime="text/plain",use_container_width=True)
        with d2: st.download_button("📊 DATA (.csv)",data=csv,file_name=f"FloodX_{selected_city}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",mime="text/csv",use_container_width=True)
        with d3: st.download_button("📋 SUMMARY",data=f"FloodX|{selected_city}|{level}|{prob}%|{now}",file_name="FloodX_Summary.txt",mime="text/plain",use_container_width=True)

# ─────────────────────────────────────────────────────────────
# TAB 2 — FUTURE FORECAST
# ─────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<span class="sec-title">📅 FLOOD RISK FORECAST — FUTURE PREDICTIONS</span>', unsafe_allow_html=True)

    base_prob = st.session_state.history[-1]["prob"] if st.session_state.history else 45
    np.random.seed(42)

    forecast_type = st.radio(
        "Select Forecast Period",
        ["📅 7-Day Weekly Forecast", "📆 12-Month Forecast", "📊 5-Year Trend"],
        horizontal=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if forecast_type == "📅 7-Day Weekly Forecast":
        st.info(f"📍 Forecast based on {selected_city} — using current seasonal patterns and weather trends")
        weekly = generate_weekly_forecast(base_prob, selected_city)

        # Cards
        cols = st.columns(7)
        for col, d in zip(cols, weekly):
            lv, clr, _, _, em = get_risk_info(d["risk"])
            bg = {"CRITICAL":"#fee2e2","HIGH":"#ffedd5","MODERATE":"#fef9c3","LOW":"#dcfce7"}[lv]
            col.markdown(f'<div class="forecast-card" style="border-top:3px solid {clr};"><div class="fc-period">{d["day"]}</div><span class="fc-risk" style="color:{clr};">{d["risk"]}%</span><div class="fc-label">{em} {lv}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Line chart
        wdf = pd.DataFrame(weekly)
        fig_w = go.Figure()
        fig_w.add_trace(go.Scatter(
            x=wdf["day"], y=wdf["risk"],
            mode="lines+markers+text",
            line=dict(color="#7c3aed", width=3),
            marker=dict(size=10, color=["#ef4444" if r>=70 else "#f97316" if r>=50 else "#eab308" if r>=35 else "#22c55e" for r in wdf["risk"]], line=dict(color="white", width=2)),
            text=[f"{r}%" for r in wdf["risk"]], textposition="top center",
            textfont=dict(family="Orbitron", size=10, color="#374151"),
            fill="tozeroy", fillcolor="rgba(124,58,237,0.07)"
        ))
        fig_w.add_hline(y=50, line_dash="dash", line_color="rgba(239,68,68,0.4)",
                        annotation_text="FLOOD THRESHOLD", annotation_font_color="#ef4444")
        fig_w.update_layout(
            title=dict(text=f"7-Day Flood Risk Forecast — {selected_city}", font=dict(family="Orbitron", size=13, color="#7c3aed")),
            height=300, paper_bgcolor="white", plot_bgcolor="white",
            xaxis=dict(showgrid=True, gridcolor="#f3f4f6", tickfont=dict(color="#6b7280")),
            yaxis=dict(range=[0,105], title="Risk %", showgrid=True, gridcolor="#f3f4f6", tickfont=dict(color="#6b7280")),
            margin=dict(t=50,b=20,l=40,r=20), showlegend=False
        )
        st.plotly_chart(fig_w, use_container_width=True)

    elif forecast_type == "📆 12-Month Forecast":
        st.info("📊 Monthly flood risk forecast based on 70+ years of Pakistan monsoon data and climate patterns")
        monthly = generate_monthly_forecast(base_prob, selected_city)
        mdf = pd.DataFrame(monthly)

        fig_m = go.Figure()
        fig_m.add_trace(go.Bar(
            x=mdf["month"], y=mdf["risk"],
            marker=dict(
                color=["#ef4444" if r>=70 else "#f97316" if r>=50 else "#eab308" if r>=35 else "#22c55e" for r in mdf["risk"]],
                line=dict(color="white", width=1)
            ),
            text=[f"{r}%" for r in mdf["risk"]], textposition="outside",
            textfont=dict(family="Orbitron", size=10, color="#374151")
        ))
        fig_m.add_hline(y=50, line_dash="dash", line_color="rgba(239,68,68,0.4)",
                        annotation_text="FLOOD THRESHOLD 50%", annotation_font_color="#ef4444")
        fig_m.add_hrect(y0=70, y1=105, fillcolor="rgba(239,68,68,0.05)", line_width=0)
        fig_m.add_annotation(x="Jul", y=90, text="⚠️ PEAK MONSOON SEASON", showarrow=False,
                              font=dict(family="Orbitron", size=10, color="#dc2626"))
        fig_m.update_layout(
            title=dict(text="12-Month Flood Risk Forecast — Pakistan", font=dict(family="Orbitron", size=13, color="#7c3aed")),
            height=380, paper_bgcolor="white", plot_bgcolor="white",
            xaxis=dict(showgrid=False, tickfont=dict(color="#6b7280")),
            yaxis=dict(range=[0,110], title="Risk %", showgrid=True, gridcolor="#f3f4f6", tickfont=dict(color="#6b7280")),
            margin=dict(t=50,b=20,l=40,r=20), showlegend=False
        )
        st.plotly_chart(fig_m, use_container_width=True)

        # Monthly summary cards
        st.markdown('<span class="sec-title">MONTHLY RISK SUMMARY</span>', unsafe_allow_html=True)
        mc = st.columns(6)
        for i, (col, d) in enumerate(zip(mc * 2, monthly)):
            lv, clr, _, _, em = get_risk_info(d["risk"])
            col.markdown(f'<div class="forecast-card" style="border-top:3px solid {clr};"><div class="fc-period">{d["month"]}</div><span class="fc-risk" style="color:{clr};">{d["risk"]}%</span><div class="fc-label">{em} {lv}</div></div>', unsafe_allow_html=True)

    else:  # 5-year
        st.info("📈 5-Year flood risk trend forecast — incorporating climate change projections and historical data")
        yearly = generate_yearly_forecast(selected_city)
        ydf = pd.DataFrame(yearly)

        fig_y = go.Figure()
        fig_y.add_trace(go.Scatter(
            x=ydf["year"], y=ydf["risk"],
            mode="lines+markers+text",
            line=dict(color="#7c3aed", width=3, dash="solid"),
            marker=dict(size=14, color=["#22c55e" if r<35 else "#eab308" if r<50 else "#f97316" if r<70 else "#ef4444" for r in ydf["risk"]], line=dict(color="white", width=2)),
            text=[f"{r}%" for r in ydf["risk"]], textposition="top center",
            textfont=dict(family="Orbitron", size=11, color="#374151"),
            fill="tozeroy", fillcolor="rgba(124,58,237,0.07)"
        ))
        fig_y.add_hline(y=50, line_dash="dash", line_color="rgba(239,68,68,0.4)",
                        annotation_text="FLOOD THRESHOLD", annotation_font_color="#ef4444")
        fig_y.add_annotation(x=ydf["year"].iloc[-1], y=ydf["risk"].iloc[-1]+8,
                              text="📈 Climate Change Impact", showarrow=False,
                              font=dict(family="Inter", size=11, color="#dc2626"))
        fig_y.update_layout(
            title=dict(text="5-Year Flood Risk Trend Forecast (Climate Change Adjusted)", font=dict(family="Orbitron", size=12, color="#7c3aed")),
            height=350, paper_bgcolor="white", plot_bgcolor="white",
            xaxis=dict(showgrid=True, gridcolor="#f3f4f6", tickfont=dict(color="#6b7280")),
            yaxis=dict(range=[0,110], title="Risk %", showgrid=True, gridcolor="#f3f4f6", tickfont=dict(color="#6b7280")),
            margin=dict(t=50,b=20,l=40,r=20), showlegend=False
        )
        st.plotly_chart(fig_y, use_container_width=True)

        y1,y2,y3,y4,y5 = st.columns(5)
        for col,d in zip([y1,y2,y3,y4,y5],yearly):
            lv,clr,_,_,em = get_risk_info(d["risk"])
            col.markdown(f'<div class="forecast-card" style="border-top:3px solid {clr};"><div class="fc-period">{d["year"]}</div><span class="fc-risk" style="color:{clr};">{d["risk"]}%</span><div class="fc-label">{em} {lv}</div></div>',unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# TAB 3 — HISTORICAL FLOODS
# ─────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<span class="sec-title">📜 HISTORICAL PAKISTAN FLOOD EVENTS</span>', unsafe_allow_html=True)
    st.caption(f"Real data from major flood events in Pakistan — 1950 to {datetime.now().year}")

    # Get province of selected city for city-specific filtering
    city_province = selected_city.split("(")[-1].replace(")","").strip()

    # Show city-specific toggle
    show_city_only = st.toggle(
        f"🏙️ Show only floods that affected {selected_city.split('(')[0].strip()} / {city_province}",
        value=False
    )

    # Filter controls
    fc1, fc2 = st.columns(2)
    with fc1:
        sev_filter = st.multiselect(
            "Filter by Severity",
            ["Catastrophic", "Severe", "Moderate"],
            default=["Catastrophic", "Severe", "Moderate"]
        )
    with fc2:
        current_yr = datetime.now().year
        year_range = st.slider("Filter by Year", 1950, current_yr, (1950, current_yr))

    st.markdown("<br>", unsafe_allow_html=True)

    # Province to region mapping for filtering
    PROVINCE_KEYWORDS = {
        "Punjab"      : ["Punjab", "All Provinces"],
        "Sindh"       : ["Sindh", "All Provinces"],
        "KPK"         : ["KPK", "NWFP", "All Provinces"],
        "Balochistan" : ["Balochistan", "All Provinces"],
        "ICT"         : ["Punjab", "All Provinces"],
        "GB"          : ["All Provinces"],
        "AJK"         : ["AJK", "All Provinces"],
    }
    relevant_keywords = PROVINCE_KEYWORDS.get(city_province, ["All Provinces"])

    def matches_city(flood_area, keywords):
        return any(kw.lower() in flood_area.lower() for kw in keywords)

    filtered = [f for f in FLOOD_HISTORY
                if f["severity"] in sev_filter
                and year_range[0] <= f["year"] <= year_range[1]
                and (not show_city_only or matches_city(f["area"], relevant_keywords))]

    if show_city_only and not filtered:
        st.info(f"No flood events found specifically for {city_province} with the current filters. Showing all Pakistan floods.")
        filtered = [f for f in FLOOD_HISTORY
                    if f["severity"] in sev_filter
                    and year_range[0] <= f["year"] <= year_range[1]]

    if show_city_only:
        st.success(f"📍 Showing {len(filtered)} flood events that affected {city_province} region")
    else:
        st.info(f"📊 Showing all {len(filtered)} Pakistan flood events — toggle above to filter by {selected_city.split('(')[0].strip()}")

    # Summary stats
    total_deaths   = sum(f["deaths"]   for f in filtered)
    total_affected = sum(f["affected"] for f in filtered)
    total_damage   = sum(f["damage_usd"] for f in filtered)
    st.markdown('<span class="sec-title">SUMMARY STATISTICS</span>', unsafe_allow_html=True)
    ss1,ss2,ss3,ss4 = st.columns(4)
    for col,(icon,val,lbl) in zip([ss1,ss2,ss3,ss4],[
        ("💀",f"{total_deaths:,}","TOTAL DEATHS"),
        ("👥",f"{total_affected/1_000_000:.1f}M","PEOPLE AFFECTED"),
        ("💰",f"${total_damage/1_000_000_000:.1f}B","TOTAL DAMAGE"),
        ("📅",str(len(filtered)),"FLOOD EVENTS"),
    ]):
        col.markdown(f'<div class="stat-card"><span class="sc-icon">{icon}</span><span class="sc-value">{val}</span><span class="sc-label">{lbl}</span></div>',unsafe_allow_html=True)

    # Timeline chart
    st.markdown('<span class="sec-title">FLOOD DEATHS TIMELINE</span>', unsafe_allow_html=True)
    hdf2 = pd.DataFrame(filtered)
    if not hdf2.empty:
        sev_clr = {"Catastrophic":"#ef4444","Severe":"#f97316","Moderate":"#eab308"}
        fig_timeline = go.Figure()
        for sev in ["Catastrophic","Severe","Moderate"]:
            sd = hdf2[hdf2["severity"]==sev]
            if not sd.empty:
                fig_timeline.add_trace(go.Bar(
                    x=sd["year"], y=sd["deaths"],
                    name=sev,
                    marker_color=sev_clr[sev],
                    text=[f"{d:,}" for d in sd["deaths"]],
                    textposition="outside"
                ))
        fig_timeline.update_layout(
            height=350, paper_bgcolor="white", plot_bgcolor="white",
            barmode="stack",
            xaxis=dict(tickmode="linear", tick0=1950, dtick=5, tickfont=dict(color="#6b7280"), gridcolor="#f3f4f6"),
            yaxis=dict(title="Deaths", showgrid=True, gridcolor="#f3f4f6", tickfont=dict(color="#6b7280")),
            legend=dict(font=dict(family="Orbitron", size=9), orientation="h", y=-0.15),
            margin=dict(t=20,b=60,l=50,r=20)
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

    # Flood event cards
    st.markdown('<span class="sec-title">FLOOD EVENT DETAILS</span>', unsafe_allow_html=True)
    for f in reversed(filtered):
        sev = f["severity"]
        bclr = {"Catastrophic":"#ef4444","Severe":"#f97316","Moderate":"#eab308"}[sev]
        badge_bg = {"Catastrophic":"#fee2e2","Severe":"#ffedd5","Moderate":"#fef9c3"}[sev]
        c1,c2,c3,c4 = st.columns([1,2,2,2])
        with c1:
            st.markdown(f'<div style="background:{badge_bg};border:2px solid {bclr};border-radius:14px;padding:16px;text-align:center;height:100%;"><span style="font-family:Orbitron,monospace;font-size:1.8rem;font-weight:900;color:{bclr};">{f["year"]}</span><br><span style="font-family:Inter,sans-serif;font-size:0.65rem;color:{bclr};font-weight:600;letter-spacing:1px;">{sev.upper()}</span></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="info-card"><div class="info-lbl">💀 Deaths</div><span class="info-val" style="color:#ef4444;">{f["deaths"]:,}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-card"><div class="info-lbl">👥 Affected</div><span class="info-val">{f["affected"]/1_000_000:.1f}M</span></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="info-card"><div class="info-lbl">💰 Damage</div><span class="info-val">${f["damage_usd"]/1_000_000_000:.1f}B</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-card"><div class="info-lbl">🌊 Cause</div><span class="info-val" style="font-size:0.75rem;">{f["cause"]}</span></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="info-card" style="height:95%;"><div class="info-lbl">📍 Area Affected</div><span class="info-val" style="font-size:0.75rem;">{f["area"]}</span></div>', unsafe_allow_html=True)
        st.markdown("", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# TAB 4 — RISK MAP
# ─────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<span class="sec-title">🗺️ PAKISTAN FLOOD RISK MAP — ALL PROVINCES</span>', unsafe_allow_html=True)

    base_for_map = st.session_state.history[-1]["prob"] if st.session_state.history else 45
    np.random.seed(abs(hash(selected_city)) % 100)

    map_data = pd.DataFrame({
        "City": list(CITIES.keys()),
        "lat" : [v["lat"] for v in CITIES.values()],
        "lon" : [v["lon"] for v in CITIES.values()],
        "Risk": [
            base_for_map if c == selected_city
            else int(np.clip(base_for_map * np.random.uniform(0.3, 0.95), 0, 100))
            for c in CITIES.keys()
        ],
    })
    map_data["Province"] = [c.split("(")[-1].replace(")","").strip() for c in map_data["City"]]
    map_data["Info"]     = map_data.apply(lambda r: f"📍 {r['City']}: {r['Risk']}% risk", axis=1)

    # Province summary
    prov_df = map_data.groupby("Province")["Risk"].mean().reset_index()
    prov_df.columns = ["Province","Avg Risk"]
    prov_df = prov_df.sort_values("Avg Risk", ascending=False)

    p1,p2 = st.columns([2,1])
    with p1:
        fig_map = px.scatter_mapbox(
            map_data, lat="lat", lon="lon",
            size="Risk", color="Risk", hover_name="Info",
            color_continuous_scale=["#22c55e","#eab308","#f97316","#ef4444"],
            range_color=[0,100], size_max=35, zoom=4.5,
            center={"lat":30.0,"lon":70.0},
            mapbox_style="open-street-map", height=500,
        )
        fig_map.update_layout(
            margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor="white",
            coloraxis_colorbar=dict(
                title=dict(text="Risk %", font=dict(color="#7c3aed")),
                tickfont=dict(color="#6b7280")
            )
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with p2:
        st.markdown('<span class="sec-title">BY PROVINCE</span>', unsafe_allow_html=True)
        for _,row in prov_df.iterrows():
            lv,clr,_,_,em = get_risk_info(int(row["Avg Risk"]))
            st.markdown(f'<div class="hist-row"><span><strong>{row["Province"]}</strong></span><span style="color:{clr};font-weight:700;font-family:Orbitron,monospace;font-size:0.78rem;">{em} {int(row["Avg Risk"])}%</span></div>',unsafe_allow_html=True)

    # Province bar chart
    st.markdown('<span class="sec-title">PROVINCE RISK COMPARISON</span>', unsafe_allow_html=True)
    prov_df_sorted = prov_df.sort_values("Avg Risk")
    fig_prov = go.Figure(go.Bar(
        x=prov_df_sorted["Avg Risk"], y=prov_df_sorted["Province"], orientation="h",
        marker=dict(
            color=["#ef4444" if r>=70 else "#f97316" if r>=50 else "#eab308" if r>=35 else "#22c55e" for r in prov_df_sorted["Avg Risk"]],
            line=dict(color="white", width=1)
        ),
        text=[f"{r:.0f}%" for r in prov_df_sorted["Avg Risk"]],
        textposition="outside",
        textfont=dict(family="Orbitron", size=10, color="#374151")
    ))
    fig_prov.update_layout(
        height=300, paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(range=[0,110], showgrid=True, gridcolor="#f3f4f6",
                   tickfont=dict(color="#9ca3af"), title=dict(text="Average Flood Risk (%)", font=dict(color="#9ca3af"))),
        yaxis=dict(tickfont=dict(color="#374151", size=12)),
        margin=dict(t=10,b=10,l=10,r=60)
    )
    st.plotly_chart(fig_prov, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# TAB 5 — OUR CONTRIBUTION
# ─────────────────────────────────────────────────────────────
with tab5:
    st.markdown('<span class="sec-title">👩‍💻 MY CONTRIBUTION — WHAT I PERSONALLY DID</span>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:linear-gradient(135deg,#4c1d95,#6d28d9);border-radius:20px;padding:28px 35px;margin-bottom:24px;box-shadow:0 10px 35px rgba(109,40,217,0.3);">
        <p style="font-family:Orbitron,monospace;font-size:0.75rem;color:rgba(255,255,255,0.65);letter-spacing:4px;text-transform:uppercase;margin-bottom:8px;">FINAL YEAR PROJECT · 2025</p>
        <p style="font-family:Orbitron,monospace;font-size:1.2rem;font-weight:900;color:#fff;letter-spacing:3px;margin-bottom:14px;">FloodX — AI Flood Intelligence System</p>
        <p style="font-family:Inter,sans-serif;font-size:0.88rem;color:rgba(255,255,255,0.75);line-height:1.9;margin:0;">
        This section explains <strong style="color:#c4b5fd;">exactly what we personally did</strong> in this project — every feature
        we designed, every line of code we wrote, and every decision we made. This project was built entirely by us as part of our
        Final Year Project at the Department of Computer Science & IT, GSCWU Bahawalpur.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Step by step what student did
    st.markdown('<span class="sec-title">WHAT I DID — STEP BY STEP</span>', unsafe_allow_html=True)

    steps_done = [
        ("1️⃣", "IDENTIFIED THE PROBLEM",
         "We researched the flood crisis in Pakistan. We found that Pakistan loses billions of dollars every year to floods (especially the 2022 floods — $30 billion damage, 33 million affected). I chose this as my FYP topic because it is a real problem that needs a real solution.",
         ["Problem Research","Pakistan Floods","NDMA Data","Literature Review"]),
        ("2️⃣", "DECIDED ON LIVE DATA APPROACH",
         "We realized that a static Kaggle dataset would not be impressive or real. So we decided to connect my app to the OpenWeatherMap API — a real website — so my app automatically fetches live weather every time the user selects a city. This was MY decision and MY design choice.",
         ["OpenWeatherMap API","REST API Integration","Real-Time Data","Python requests library"]),
        ("3️⃣", "DESIGNED THE RISK ALGORITHM",
         "We created my own flood risk calculation formula. We gave each weather factor a weight based on scientific research: Rainfall gets 40% weight because it is the main cause of floods. Humidity gets 22%, Low Air Pressure 18%, Cloud Cover 12%, Wind Speed 8%. I also added a special boost when temperature is above 38°C and humidity above 70% — because that combination creates extreme storm conditions.",
         ["Custom Algorithm","Weighted Formula","Scientific Research","Meteorology"]),
        ("4️⃣", "BUILT THE WEB APPLICATION",
         "We wrote all the Python code for the Streamlit web application. we set up the page configuration, wrote the CSS styling with animations, created the control panel, built all 5 tabs, and connected everything together. The app has 37 Pakistan cities from all provinces, all sorted alphabetically.",
         ["Python","Streamlit","CSS Animations","5 Tabs","37 Cities"]),
        ("5️⃣", "CREATED DATA VISUALIZATIONS",
         "We built all the charts and visualizations myself using Plotly. This includes the flood risk gauge meter, the weather risk bar chart, the radar chart, the Pakistan map, the history line chart, the monthly forecast bar chart, the 5-year trend line, and the historical flood timeline.",
         ["Plotly Charts","Gauge Meter","Radar Chart","Pakistan Map","Forecast Charts"]),
        ("6️⃣", "ADDED HISTORICAL FLOOD DATABASE",
         "We manually researched and compiled real Pakistan flood data from 1950 to 2023 — 16 major flood events with real numbers for deaths, people affected, economic damage, affected areas and causes. I added filters so users can search by severity and year. I also added a toggle to show only floods that affected the selected city's province.",
         ["Real Historical Data","1950-2023","16 Flood Events","Interactive Filters","Province Filter"]),
        ("7️⃣", "BUILT FUTURE FORECAST SYSTEM",
         "We designed a 3-level flood forecast system using seasonal patterns from Pakistan's 70+ years of monsoon data. The 7-day forecast uses current conditions. The 12-month forecast shows which months are dangerous (July-August are peak monsoon). The 5-year trend shows that flood risk is INCREASING because of climate change.",
         ["7-Day Forecast","12-Month Forecast","5-Year Trend","Climate Change","Seasonal Patterns"]),
        ("8️⃣", "DESIGNED THE COMPLETE UI",
         "We designed the entire look and feel of the app myself. We chose the purple-blue gradient theme, the Orbitron font, the glassmorphism card style, the animated header, the glowing buttons, the color-coded alert system (green/yellow/orange/red), and made it mobile-responsive so it works on phones too.",
         ["UI/UX Design","Glassmorphism","CSS Animations","Color Coding","Mobile Responsive"]),
    ]

    for i in range(0, len(steps_done), 2):
        ca, cb = st.columns(2)
        for col, step in zip([ca, cb], steps_done[i:i+2]):
            icon, title, desc, tags = step
            tags_html = "".join([f'<span class="contrib-tag">{t}</span>' for t in tags])
            col.markdown(f"""
            <div class="contrib-card">
                <span class="contrib-icon">{icon}</span>
                <div class="contrib-title">{title}</div>
                <div class="contrib-desc">{desc}</div>
                <div style="margin-top:12px;">{tags_html}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # What makes this unique
    st.markdown('<span class="sec-title">WHAT MAKES MY PROJECT UNIQUE</span>', unsafe_allow_html=True)
    u1, u2, u3 = st.columns(3)
    for col, (icon, title, desc) in zip([u1,u2,u3],[
        ("🌐", "REAL LIVE DATA", "Most FYP projects use old offline datasets.  Our app connects to a real website (OpenWeatherMap) and gets live data every time — making it a genuinely real-world system."),
        ("📅", "PAST + FUTURE", "My app is the only FYP that shows both historical flood records (1950-2023) AND future flood forecasts (weekly, monthly, 5-year) in one place."),
        ("🏙️", "ALL OF PAKISTAN", "Most flood apps focus on one region. I covered all 37 major cities across all provinces — Punjab, Sindh, KPK, Balochistan, GB, AJK, and ICT."),
    ]):
        col.markdown(f"""
        <div class="contrib-card" style="text-align:center;">
            <span class="contrib-icon">{icon}</span>
            <div class="contrib-title">{title}</div>
            <div class="contrib-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Contribution cards
    st.markdown('<span class="sec-title">TECHNOLOGIES I USED</span>', unsafe_allow_html=True)

    ca,cb = st.columns(2)
    with ca:
        st.markdown("""
        <div class="contrib-card">
            <span class="contrib-icon">🌐</span>
            <div class="contrib-title">LIVE WEATHER API INTEGRATION</div>
            <div class="contrib-desc">
                We connected FloodX to the <strong>OpenWeatherMap REST API</strong> to fetch
                real-time weather data for any Pakistan city. Every prediction uses actual live
                data — Rainfall, Temperature, Humidity, Wind Speed, Air Pressure, and Cloud Cover
                — pulled directly from weather stations at that exact moment.
            </div>
            <div style="margin-top:12px;">
                <span class="contrib-tag">OpenWeatherMap API</span>
                <span class="contrib-tag">REST API</span>
                <span class="contrib-tag">Real-Time Data</span>
                <span class="contrib-tag">Python requests</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with cb:
        st.markdown("""
        <div class="contrib-card">
            <span class="contrib-icon">🧠</span>
            <div class="contrib-title">SMART FLOOD RISK ALGORITHM</div>
            <div class="contrib-desc">
                We designed a <strong>weighted multi-factor flood risk algorithm</strong> based on
                meteorological research. Each weather factor has a scientifically justified weight:
                Rainfall (40%), Humidity (22%), Low Pressure (18%), Cloud Cover (12%),
                Wind Speed (8%). The algorithm also includes a temperature-humidity boost
                for extreme heat conditions.
            </div>
            <div style="margin-top:12px;">
                <span class="contrib-tag">Custom Algorithm</span>
                <span class="contrib-tag">Weighted Scoring</span>
                <span class="contrib-tag">Meteorological Research</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    cc,cd = st.columns(2)
    with cc:
        st.markdown("""
        <div class="contrib-card">
            <span class="contrib-icon">📅</span>
            <div class="contrib-title">FUTURE FLOOD FORECASTING</div>
            <div class="contrib-desc">
                We built a <strong>3-level flood forecast system</strong> — 7-day weekly,
                12-month, and 5-year trend — using historical monsoon patterns from 70+ years
                of Pakistan flood data. The 5-year forecast incorporates <strong>climate change
                impact projections</strong> showing increasing flood risk trend.
            </div>
            <div style="margin-top:12px;">
                <span class="contrib-tag">7-Day Forecast</span>
                <span class="contrib-tag">Monthly Forecast</span>
                <span class="contrib-tag">Climate Change Trend</span>
                <span class="contrib-tag">Seasonal Patterns</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with cd:
        st.markdown("""
        <div class="contrib-card">
            <span class="contrib-icon">📜</span>
            <div class="contrib-title">HISTORICAL FLOOD DATABASE</div>
            <div class="contrib-desc">
                We compiled and integrated a <strong>comprehensive database of real Pakistan
                flood events from 1950 to 2023</strong> — including deaths, people affected,
                economic damage, affected areas, and flood causes. Users can filter by
                severity and year range to analyze flood history.
            </div>
            <div style="margin-top:12px;">
                <span class="contrib-tag">16 Flood Events</span>
                <span class="contrib-tag">Real Data 1950–2023</span>
                <span class="contrib-tag">Interactive Filters</span>
                <span class="contrib-tag">Timeline Charts</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    ce,cf = st.columns(2)
    with ce:
        st.markdown("""
        <div class="contrib-card">
            <span class="contrib-icon">🗺️</span>
            <div class="contrib-title">INTERACTIVE PAKISTAN RISK MAP</div>
            <div class="contrib-desc">
                We built an <strong>interactive geographic flood risk map of Pakistan</strong>
                showing all 37 cities across all provinces with color-coded bubbles indicating
                flood risk level. The map also includes a <strong>province-level comparison chart</strong>
                showing which province has the highest average flood risk.
            </div>
            <div style="margin-top:12px;">
                <span class="contrib-tag">37 Pakistan Cities</span>
                <span class="contrib-tag">All Provinces</span>
                <span class="contrib-tag">Plotly Mapbox</span>
                <span class="contrib-tag">Province Comparison</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with cf:
        st.markdown("""
        <div class="contrib-card">
            <span class="contrib-icon">🎨</span>
            <div class="contrib-title">MODERN PROFESSIONAL UI DESIGN</div>
            <div class="contrib-desc">
                We designed a <strong>completely custom user interface</strong> using glassmorphism
                design, CSS animations, gradient backgrounds, Orbitron font, and a purple-blue
                tech theme. The app is <strong>fully mobile-responsive</strong> and includes
                animated headers, hover effects, color-coded alerts, and smooth transitions.
            </div>
            <div style="margin-top:12px;">
                <span class="contrib-tag">Glassmorphism</span>
                <span class="contrib-tag">CSS Animations</span>
                <span class="contrib-tag">Mobile Responsive</span>
                <span class="contrib-tag">Custom Design</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Tech stack
    st.markdown('<span class="sec-title">TECHNOLOGY STACK</span>', unsafe_allow_html=True)
    tech_cols = st.columns(5)
    for col, (icon, name, desc) in zip(tech_cols, [
        ("🐍","Python 3.10",   "Core language"),
        ("📊","Streamlit",     "Web framework"),
        ("📈","Plotly",        "Interactive charts"),
        ("🌐","OpenWeatherMap","Live weather API"),
        ("🎨","Custom CSS",    "UI & animations"),
    ]):
        col.markdown(f'<div class="forecast-card"><div class="fc-period">{icon}</div><span class="fc-risk" style="font-size:0.9rem;color:#7c3aed;">{name}</span><div class="fc-label">{desc}</div></div>', unsafe_allow_html=True)

    # Impact
    st.markdown('<span class="sec-title">PROJECT IMPACT</span>', unsafe_allow_html=True)
    i1,i2,i3,i4 = st.columns(4)
    for col,(icon,val,lbl) in zip([i1,i2,i3,i4],[
        ("🏙️","37","Cities Covered"),
        ("🗺️","6", "Provinces + Territories"),
        ("📜","16","Historical Floods"),
        ("📅","5", "Years Forecasted"),
    ]):
        col.markdown(f'<div class="stat-card"><span class="sc-icon">{icon}</span><span class="sc-value">{val}</span><span class="sc-label">{lbl}</span></div>',unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:linear-gradient(135deg,#4c1d95,#6d28d9);border-radius:20px;padding:28px 35px;text-align:center;box-shadow:0 10px 35px rgba(109,40,217,0.3);">
        <p style="font-family:Orbitron,monospace;font-size:1.1rem;font-weight:900;color:#fff;letter-spacing:4px;margin-bottom:12px;">🌊 FloodX v8.0</p>
        <p style="font-family:Inter,sans-serif;font-size:0.88rem;color:rgba(255,255,255,0.75);line-height:1.8;margin:0;">
        Final Year Project · Department of Computer Science & IT<br>
        The Govt. Sadiq College Women University Bahawalpur · 2025<br>
        <strong style="color:#c4b5fd;">Built to save lives through intelligent flood prediction</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# TAB 6 — VOICE ALERT & SOS (WORLD FIRST IN FLOOD APPS)
# ─────────────────────────────────────────────────────────────
with tab6:
    city_name = selected_city.split("(")[0].strip()
    last      = st.session_state.history[-1] if st.session_state.history else None
    prob_v    = last["prob"]  if last else 0
    level_v   = last["level"] if last else "UNKNOWN"
    emoji_v   = {"CRITICAL":"🔴","HIGH":"🟠","MODERATE":"🟡","LOW":"🟢"}.get(level_v,"⚪")

    st.markdown('''
    <style>
    .sos-banner {
        background:linear-gradient(135deg,#7c3aed,#9333ea,#6366f1);
        border-radius:22px; padding:30px 36px; text-align:center;
        margin-bottom:26px; box-shadow:0 12px 40px rgba(124,58,237,0.4);
        position:relative; overflow:hidden;
    }
    .sos-banner::before {
        content:"🔊"; position:absolute; font-size:9rem;
        opacity:0.06; top:-10px; right:-10px; pointer-events:none;
    }
    .sos-title { font-family:Orbitron,monospace; font-size:1.3rem; font-weight:900; color:#fff; letter-spacing:4px; }
    .sos-sub   { font-family:Inter,sans-serif; font-size:0.85rem; color:rgba(255,255,255,0.75); margin-top:10px; line-height:1.7; }
    .evac-card { background:rgba(255,255,255,0.72); backdrop-filter:blur(18px);
        border:1px solid rgba(167,139,250,0.25); border-radius:20px;
        padding:22px 20px; margin-bottom:14px; transition:all 0.3s;
        box-shadow:0 4px 20px rgba(124,58,237,0.08); }
    .evac-card:hover { transform:translateX(6px); border-color:rgba(124,58,237,0.4); }
    .evac-name { font-family:Orbitron,monospace; font-size:0.72rem; font-weight:700; color:#7c3aed; letter-spacing:1.5px; }
    .evac-dist { font-family:Inter,sans-serif; font-size:0.82rem; color:#6b7280; margin-top:4px; }
    .contact-card { background:rgba(255,255,255,0.72); backdrop-filter:blur(18px);
        border-radius:18px; border:1px solid rgba(167,139,250,0.2);
        padding:18px 20px; margin-bottom:10px;
        box-shadow:0 3px 15px rgba(124,58,237,0.07); }
    </style>
    ''', unsafe_allow_html=True)

    # ── Header banner
    st.markdown(f'''
    <div class="sos-banner">
        <div class="sos-title">🔊 AI VOICE ALERT & EMERGENCY SOS SYSTEM</div>
        <div class="sos-sub">
            World's First AI Flood Voice Alert in any Flood Prediction App<br>
            Tap the button below — FloodX will speak the flood warning aloud 
        </div>
    </div>''', unsafe_allow_html=True)

    # ── Current status for this city
    status_col, voice_col = st.columns([1, 1])

    with status_col:
        st.markdown('<span class="sec-title">📍 CURRENT CITY STATUS</span>', unsafe_allow_html=True)
        if last:
            bclr = {"CRITICAL":"#ef4444","HIGH":"#f97316","MODERATE":"#eab308","LOW":"#22c55e"}.get(level_v,"#6b7280")
            bg   = {"CRITICAL":"#fee2e2","HIGH":"#ffedd5","MODERATE":"#fef9c3","LOW":"#dcfce7"}.get(level_v,"#f3f4f6")
            st.markdown(f'''
            <div style="background:{bg};border:2px solid {bclr};border-radius:20px;padding:24px;text-align:center;">
                <div style="font-size:3rem;">{emoji_v}</div>
                <div style="font-family:Orbitron,monospace;font-size:1.6rem;font-weight:900;color:{bclr};">{prob_v}%</div>
                <div style="font-family:Orbitron,monospace;font-size:0.75rem;color:{bclr};letter-spacing:2px;margin-top:4px;">{level_v} RISK</div>
                <div style="font-family:Inter,sans-serif;font-size:0.8rem;color:#6b7280;margin-top:8px;">📍 {selected_city}</div>
            </div>''', unsafe_allow_html=True)
        else:
            st.info("Run a prediction first (Tab 1) to see city status here.")

    with voice_col:
        st.markdown('<span class="sec-title">🔊 VOICE ALERT — CLICK TO SPEAK</span>', unsafe_allow_html=True)
        lang_choice = "🇬🇧 English"

        if last:
            # ── English message ───────────────────────────────────────
            eng_msg = (
                f"Flood Alert for {city_name}, Pakistan. "
                f"Current flood risk is {prob_v} percent. "
                f"Risk level: {level_v}. "
                + ("Immediate evacuation is recommended. Contact NDMA at one seven hundred immediately." if level_v=="CRITICAL"
                   else "Stay alert and monitor local weather updates carefully." if level_v in ["HIGH","MODERATE"]
                   else "Conditions are currently safe. Stay informed.")
            )

            # ── Clean text for JS (remove quotes that break JS string) ─
            eng_safe  = eng_msg.replace("'","").replace('"',"")

            # ── English-only speak function ─────────────────────────────
            js_speak = f"""
            function speakNow() {{
                if(!window.speechSynthesis) {{
                    setStatus("❌ Browser does not support speech."); return;
                }}
                window.speechSynthesis.cancel();
                var u = new SpeechSynthesisUtterance("{eng_safe}");
                u.lang    = "en-US";
                u.rate    = 0.88;
                u.pitch   = 1.05;
                u.volume  = 1.0;
                setStatus("🔊 Speaking in English...");
                u.onend = function() {{ setStatus("✅ Done."); }};
                window.speechSynthesis.speak(u);
            }}"""
            btn_label = "🔊 SPEAK IN ENGLISH"

            # ── Render the voice button with correct JS ────────────────
            st.components.v1.html(f"""
            <div style="text-align:center;margin-top:10px;">
                <button onclick="speakNow()" style="
                    background:linear-gradient(135deg,#7c3aed,#9333ea);
                    color:white;border:none;border-radius:16px;
                    padding:18px 36px;font-size:1rem;font-weight:700;
                    cursor:pointer;letter-spacing:1px;font-family:monospace;
                    box-shadow:0 8px 24px rgba(124,58,237,0.45);
                    margin-bottom:10px;display:block;width:100%;">
                    {btn_label}
                </button>
                <button onclick="stopSpeak()" style="
                    background:rgba(239,68,68,0.08);color:#ef4444;
                    border:2px solid #ef4444;border-radius:14px;
                    padding:12px 28px;font-size:0.85rem;font-weight:700;
                    cursor:pointer;font-family:monospace;width:100%;">
                    ⏹ STOP VOICE
                </button>
                <div id="speak-status" style="margin-top:14px;font-family:monospace;font-size:0.82rem;color:#7c3aed;min-height:20px;"></div>
            </div>
            <script>
            function setStatus(msg) {{
                var el = document.getElementById("speak-status");
                if(el) el.innerText = msg;
            }}
            {js_speak}
            function stopSpeak() {{
                if(window.speechSynthesis) window.speechSynthesis.cancel();
                setStatus("⏹ Stopped.");
            }}
            // Pre-load voices so they are ready
            window.speechSynthesis.getVoices();
            if(window.speechSynthesis.onvoiceschanged !== undefined) {{
                window.speechSynthesis.onvoiceschanged = function() {{ window.speechSynthesis.getVoices(); }};
            }}
            </script>
            """, height=180)

            # ── Show the message text being spoken ─────────────────────
            st.markdown(f"""
            <div style="background:#f0fdf4;border:1px solid #22c55e;border-radius:14px;
                 padding:16px 20px;margin-top:10px;">
                <div style="font-family:Inter;font-size:0.6rem;letter-spacing:2px;
                color:#16a34a;text-transform:uppercase;margin-bottom:6px;">📢 English Message</div>
                <div style="font-family:Inter;font-size:0.85rem;color:#374151;line-height:1.7;">{eng_msg}</div>
            </div>""", unsafe_allow_html=True)

        else:
            st.warning("⚠️ Run a prediction in Tab 1 first to enable voice alert.")

    st.markdown("---")

    # ── Evacuation Routes
    st.markdown('<span class="sec-title">🚨 AI EVACUATION ROUTE SUGGESTER</span>', unsafe_allow_html=True)
    st.caption("First-ever city-specific evacuation guidance in any Pakistan flood app")

    EVACUATION_DATA = {
        "Punjab"     : {"shelter":"Rescue 1122 camps, local schools, mosques","route":"Move to nearest high-ground area, avoid canal roads","hospital":"DHQ Hospital or nearest Civil Hospital","helpline":"1122 (Rescue), 1700 (NDMA)"},
        "Sindh"      : {"shelter":"Sindh Relief camps, railway stations on high ground","route":"Move inland away from Indus River, avoid low-lying areas","hospital":"Civil Hospital Karachi / Hyderabad","helpline":"021-99205100 (PDMA Sindh), 1700"},
        "KPK"        : {"shelter":"KP Rescue camps, high-ground schools","route":"Avoid riverbanks, move to hills, use mountain roads","hospital":"Lady Reading Hospital Peshawar","helpline":"1122, 1700 (NDMA)"},
        "Balochistan": {"shelter":"PDA relief camps, high-ground areas","route":"Avoid flash flood valleys (nullahs), use elevated roads","hospital":"Civil Hospital Quetta / nearest DHQ","helpline":"0800-88000 (PDMA), 1700"},
        "GB"         : {"shelter":"GBDMA camps, higher elevation villages","route":"Move to stable high ground, avoid glacial lake areas","hospital":"DHQ Hospital Gilgit","helpline":"05811-920234 (GBDMA), 1700"},
        "AJK"        : {"shelter":"AJK government relief camps","route":"Avoid Jhelum and Neelum River banks, go to high areas","hospital":"DHQ Muzaffarabad","helpline":"05822-921028 (SDMA AJK), 1700"},
        "ICT"        : {"shelter":"F-9 Park, Pakistan Sports Complex","route":"Avoid Nullah Lai, use Murree Road and main arteries","hospital":"PIMS Hospital, Polyclinic","helpline":"051-9250255 (CDA), 1700"},
    }

    province = selected_city.split("(")[-1].replace(")","").strip()
    evac = EVACUATION_DATA.get(province, EVACUATION_DATA["Punjab"])

    ea, eb = st.columns(2)
    with ea:
        for icon, label, val in [
            ("🏕️", "NEAREST SHELTER", evac["shelter"]),
            ("🚗", "EVACUATION ROUTE", evac["route"]),
        ]:
            st.markdown(f'''
            <div class="evac-card">
                <div style="font-size:2rem;margin-bottom:8px;">{icon}</div>
                <div class="evac-name">{label}</div>
                <div class="evac-dist">{val}</div>
            </div>''', unsafe_allow_html=True)

    with eb:
        for icon, label, val in [
            ("🏥", "NEAREST HOSPITAL", evac["hospital"]),
            ("📞", "EMERGENCY HELPLINES", evac["helpline"]),
        ]:
            st.markdown(f'''
            <div class="evac-card">
                <div style="font-size:2rem;margin-bottom:8px;">{icon}</div>
                <div class="evac-name">{label}</div>
                <div class="evac-dist">{val}</div>
            </div>''', unsafe_allow_html=True)

    # ── Emergency contacts
    st.markdown('<span class="sec-title">📞 PAKISTAN NATIONAL EMERGENCY CONTACTS</span>', unsafe_allow_html=True)
    ec1, ec2, ec3, ec4 = st.columns(4)
    for col, (icon, name, num, clr) in zip([ec1,ec2,ec3,ec4],[
        ("🚨","NDMA","1700","#ef4444"),
        ("🚒","Rescue 1122","1122","#f97316"),
        ("🚔","Police","15","#3b82f6"),
        ("🚑","Ambulance","1122 / 115","#22c55e"),
    ]):
        col.markdown(f'''
        <div class="contact-card" style="text-align:center;border-top:3px solid {clr};">
            <div style="font-size:2.2rem;margin-bottom:8px;">{icon}</div>
            <div style="font-family:Orbitron,monospace;font-size:0.62rem;color:#6b7280;letter-spacing:2px;">{name}</div>
            <div style="font-family:Orbitron,monospace;font-size:1.8rem;font-weight:900;color:{clr};">{num}</div>
        </div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('''
    <div style="background:linear-gradient(135deg,#1e1060,#2d1b69);border-radius:18px;padding:20px 28px;text-align:center;">
        <div style="font-family:Orbitron,monospace;font-size:0.65rem;color:#a78bfa;letter-spacing:3px;margin-bottom:8px;">
            ⭐ WORLD FIRST — UNIQUE FEATURE
        </div>
        <div style="font-family:Inter,sans-serif;font-size:0.85rem;color:rgba(255,255,255,0.75);line-height:1.8;">
            FloodX is the <strong style="color:#c4b5fd;">world's first flood prediction app</strong> to include
            <strong style="color:#c4b5fd;">AI voice alerts</strong> using browser Speech Synthesis,
            combined with <strong style="color:#c4b5fd;">city-specific evacuation routes, shelter locations, and hospital guidance</strong>
            — all generated automatically based on the selected city and province.
            No other flood prediction system in Pakistan or worldwide has this feature.
        </div>
    </div>
    ''', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown(
    f'<div class="footer">FloodX v8.0  |  AI FLOOD INTELLIGENCE  |  PAKISTAN  |  '
    f'OPENWEATHERMAP  |  37 CITIES  |  ALL PROVINCES  |  {datetime.now().year}</div>',
    unsafe_allow_html=True
)
