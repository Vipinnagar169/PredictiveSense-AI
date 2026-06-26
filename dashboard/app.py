import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import os

st.set_page_config(
    page_title="PredictiveSense AI",
    page_icon="🚀",
    layout="wide"
)

# ── Load Model & Data ──────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(BASE_DIR, 'models', 'rf_optimised.pkl'), 'rb') as f:
        rf = pickle.load(f)
    with open(os.path.join(BASE_DIR, 'models', 'iso_forest.pkl'), 'rb') as f:
        iso = pickle.load(f)
    return rf, iso

@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return pd.read_csv(os.path.join(BASE_DIR, 'data', 'processed', 'train_final.csv'))
    

rf_model, iso_model = load_models()
df = load_data()

sensor_cols = [col for col in df.columns if 'sensor' in col]
feature_cols = [col for col in df.columns if col not in ['RUL','unit_id','cycle']]

# ── Header ─────────────────────────────────────────────────────────────────
st.title("🚀 PredictiveSense AI")
st.subheader("AI-Powered Predictive Sensor Monitoring & Failure Detection Platform")
st.caption("DRDO Internship 2026 | Vipin Nagar")
st.markdown("---")

# ── Metrics Row ────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Engines",   "100")
col2.metric("Total Records",   "20,631")
col3.metric("Best R2 Score",   "0.79")
col4.metric("Anomalies Found", "1,032 (5%)")
st.markdown("---")

# ── Sidebar ────────────────────────────────────────────────────────────────
st.sidebar.title("⚙️ Control Panel")
st.sidebar.markdown("### Select Engine")
engine_id = st.sidebar.slider("Engine ID", 1, 100, 1)

st.sidebar.markdown("### Select Sensor")
selected_sensor = st.sidebar.selectbox("Sensor to Monitor", sensor_cols, index=sensor_cols.index('sensor_11'))

# ── Engine Data ────────────────────────────────────────────────────────────
engine_df = df[df['unit_id'] == engine_id].copy()
last_reading = engine_df[feature_cols].iloc[-1:].values
predicted_rul = rf_model.predict(last_reading)[0]
actual_rul    = engine_df['RUL'].iloc[-1]

# Anomaly for this engine
engine_anomaly_score = iso_model.decision_function(engine_df[sensor_cols])
engine_df['anomaly_score'] = engine_anomaly_score
engine_df['is_anomaly'] = iso_model.predict(engine_df[sensor_cols])
anomaly_count = (engine_df['is_anomaly'] == -1).sum()

# ── Section 1 — Engine Health ───────────────────────────────────────────────
st.markdown("## 🔍 Engine Health Status")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Engine ID",       f"#{engine_id}")
c2.metric("Predicted RUL",   f"{predicted_rul:.0f} cycles")
c3.metric("Actual RUL",      f"{actual_rul:.0f} cycles")
c4.metric("Anomalies",       f"{anomaly_count}")

# Alert
st.markdown("### 🚨 Alert Status")
if predicted_rul <= 40:
    st.error(f"🔴 CRITICAL — Engine #{engine_id} may fail in {predicted_rul:.0f} cycles! Immediate maintenance required!")
elif predicted_rul <= 80:
    st.warning(f"🟡 WARNING — Engine #{engine_id} showing degradation. Plan maintenance. RUL: {predicted_rul:.0f} cycles")
else:
    st.success(f"🟢 HEALTHY — Engine #{engine_id} operating normally. RUL: {predicted_rul:.0f} cycles")
st.markdown("---")

# ── Section 2 — Sensor Health ───────────────────────────────────────────────
st.markdown(f"## 📊 Sensor Health Trend — {selected_sensor.upper()}")

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(engine_df['cycle'], engine_df[selected_sensor],
        color='steelblue', linewidth=1.5, label=selected_sensor)

# Mark anomalies on sensor chart
anomaly_df = engine_df[engine_df['is_anomaly'] == -1]
ax.scatter(anomaly_df['cycle'], anomaly_df[selected_sensor],
           color='red', s=30, zorder=5, label='Anomaly Detected')

ax.set_title(f'Engine #{engine_id} — {selected_sensor} Readings Over Time', fontsize=13)
ax.set_xlabel('Cycle')
ax.set_ylabel(f'{selected_sensor} (normalized)')
ax.legend()
ax.grid(True, alpha=0.3)
st.pyplot(fig)
plt.close()

st.markdown("---")

# ── Section 3 — RUL Trend ───────────────────────────────────────────────────
st.markdown("## 📉 RUL Trend — Engine Life Remaining")

fig2, ax2 = plt.subplots(figsize=(12, 4))
ax2.plot(engine_df['cycle'], engine_df['RUL'],
         color='crimson', linewidth=2, label='Actual RUL')
ax2.axhline(y=40, color='red',    linestyle='--', alpha=0.7, label='Critical Zone (40)')
ax2.axhline(y=80, color='orange', linestyle='--', alpha=0.7, label='Warning Zone (80)')
ax2.fill_between(engine_df['cycle'], 0, 40,
                 alpha=0.1, color='red', label='Danger Zone')
ax2.set_title(f'Engine #{engine_id} — RUL Over Time', fontsize=13)
ax2.set_xlabel('Cycle')
ax2.set_ylabel('RUL (cycles remaining)')
ax2.legend()
ax2.grid(True, alpha=0.3)
st.pyplot(fig2)
plt.close()

st.markdown("---")

# ── Section 4 — Anomaly Detection ───────────────────────────────────────────
st.markdown("## 🚨 Anomaly Detection Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Anomaly Score Over Time")
    fig3, ax3 = plt.subplots(figsize=(7, 4))
    ax3.plot(engine_df['cycle'], engine_df['anomaly_score'],
             color='steelblue', linewidth=1.5, label='Anomaly Score')
    ax3.axhline(y=0, color='red', linestyle='--', linewidth=1.5, label='Threshold')
    ax3.fill_between(engine_df['cycle'],
                     engine_df['anomaly_score'], 0,
                     where=(engine_df['anomaly_score'] < 0),
                     color='red', alpha=0.3, label='Anomaly Zone')
    ax3.set_title(f'Engine #{engine_id} — Anomaly Score', fontsize=11)
    ax3.set_xlabel('Cycle')
    ax3.set_ylabel('Score')
    ax3.legend(fontsize=8)
    ax3.grid(True, alpha=0.3)
    st.pyplot(fig3)
    plt.close()

with col2:
    st.markdown("### Anomaly Summary")
    total   = len(engine_df)
    anom    = anomaly_count
    normal  = total - anom
    anom_pct = (anom/total)*100

    st.metric("Total Readings",    total)
    st.metric("Normal Readings",   normal)
    st.metric("Anomalies Detected", f"{anom} ({anom_pct:.1f}%)")

    if anom_pct > 10:
        st.error("🔴 High anomaly rate — check engine!")
    elif anom_pct > 5:
        st.warning("🟡 Moderate anomalies — monitor closely")
    else:
        st.success("🟢 Low anomaly rate — normal operation")

st.markdown("---")
st.caption("PredictiveSense AI | DRDO Internship 2026 | Vipin Nagar | github.com/Vipinnagar169/PredictiveSense-AI")