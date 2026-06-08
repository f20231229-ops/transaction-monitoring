"""
app.py — Streamlit Dashboard for Transaction Monitoring

A professional, dark-themed interface for uploading transaction CSVs,
running the monitoring pipeline, and viewing real-time alert metrics.
"""

import sys
import os

# Ensure project root is on the path so `src.*` imports work
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd

from src.pipeline import run_monitoring_pipeline

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Transaction Monitor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* ── Global ─────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background: linear-gradient(160deg, #0f0c29 0%, #1a1a3e 40%, #24243e 100%);
    }

    /* ── Header ─────────────────────────────────────── */
    .main-header {
        text-align: center;
        padding: 2.5rem 0 1rem;
    }
    .main-header h1 {
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00d2ff 0%, #7b2ff7 50%, #ff6fd8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }
    .main-header p {
        color: #9ca3af;
        font-size: 1.05rem;
        margin-top: 0;
    }

    /* ── Glass card ─────────────────────────────────── */
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.8rem;
        backdrop-filter: blur(12px);
        margin-bottom: 1.2rem;
    }
    .glass-card h3 {
        color: #e2e8f0;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }

    /* ── Metric cards ───────────────────────────────── */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 1.2rem 1rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(123, 47, 247, 0.15);
    }
    [data-testid="stMetricLabel"] {
        color: #9ca3af !important;
        font-weight: 500;
    }
    [data-testid="stMetricValue"] {
        font-weight: 700;
        color: #f1f5f9 !important;
    }

    /* ── Buttons ────────────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, #7b2ff7, #00d2ff);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2.5rem;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.02em;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(123, 47, 247, 0.35);
    }

    /* ── File uploader ──────────────────────────────── */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.03);
        border: 2px dashed rgba(123, 47, 247, 0.35);
        border-radius: 14px;
        padding: 1.5rem;
    }

    /* ── Alert banners ──────────────────────────────── */
    .alert-pass {
        background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(16,185,129,0.05));
        border-left: 4px solid #10b981;
        border-radius: 10px;
        padding: 1rem 1.5rem;
        color: #6ee7b7;
        font-weight: 600;
        font-size: 1.05rem;
        margin: 1rem 0;
    }
    .alert-fail {
        background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(239,68,68,0.05));
        border-left: 4px solid #ef4444;
        border-radius: 10px;
        padding: 1rem 1.5rem;
        color: #fca5a5;
        font-weight: 600;
        font-size: 1.05rem;
        margin: 1rem 0;
    }

    /* ── Divider ────────────────────────────────────── */
    .styled-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(123,47,247,0.3), transparent);
        border: none;
        margin: 1.5rem 0;
    }

    /* ── Dataframe ──────────────────────────────────── */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="main-header">
        <h1>🛡️ Transaction Monitor</h1>
        <p>Upload transaction data · Detect anomalies · Measure drift · Generate alerts</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

# ── Upload Section ───────────────────────────────────────────────────────────
st.markdown(
    '<div class="glass-card"><h3>📂 Upload Transaction File</h3></div>',
    unsafe_allow_html=True,
)
uploaded_file = st.file_uploader(
    "Drag & drop a CSV file or click to browse",
    type=["csv"],
    label_visibility="collapsed",
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Preview
    with st.expander("🔍 Preview uploaded data", expanded=False):
        st.dataframe(df.head(20), use_container_width=True)

    st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

    # ── Run Button ───────────────────────────────────────────────────────────
    col_btn = st.columns([1, 2, 1])[1]
    with col_btn:
        run_clicked = st.button("🚀  Run Monitoring", use_container_width=True)

    if run_clicked:
        with st.spinner("Running pipeline…"):
            results = run_monitoring_pipeline(df)

        st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

        # ── Metric Cards ─────────────────────────────────────────────────────
        st.markdown(
            '<div class="glass-card"><h3>📊 Pipeline Results</h3></div>',
            unsafe_allow_html=True,
        )
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Transactions", f"{results['total_transactions']:,}")
        c2.metric("Missing Data %", f"{results['missing_percent']}%")
        c3.metric("Anomalies Detected", results["anomaly_count"])
        c4.metric("Drift Score", f"{results['drift_score']}%")

        st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

        # ── Alert Banner ─────────────────────────────────────────────────────
        alert_status = results["alert"]
        if alert_status == "Healthy":
            st.markdown(
                '<div class="alert-pass">✅ ALL CLEAR — No anomalies or significant drift detected.</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="alert-fail">🚨 ALERT — {alert_status}. Review flagged transactions below.</div>',
                unsafe_allow_html=True,
            )

        # ── Drift Details ────────────────────────────────────────────────────
        with st.expander("📈 Drift Details", expanded=False):
            dc1, dc2, dc3 = st.columns(3)
            dc1.metric("Baseline Mean", f"${results['baseline_mean']:,.2f}")
            dc2.metric("Uploaded Mean", f"${results['uploaded_mean']:,.2f}")
            dc3.metric("Drift %", f"{results['drift_score']}%")

        # ── Anomaly Detail Table ─────────────────────────────────────────────
        if results["anomaly_count"] > 0:
            with st.expander(
                f"⚠️ Flagged Transactions ({results['anomaly_count']} rows)",
                expanded=True,
            ):
                st.dataframe(
                    results["anomaly_rows"],
                    use_container_width=True,
                    hide_index=True,
                )

        # ── Log confirmation ─────────────────────────────────────────────────
        st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)
        st.success("✅ Results appended to `logs/monitoring_log.csv` — ready for Tableau.")

else:
    # ── Empty state ──────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="glass-card" style="text-align:center; padding:3rem;">
            <p style="font-size:3rem; margin-bottom:0.5rem;">📤</p>
            <p style="color:#9ca3af; font-size:1.1rem;">
                Upload a CSV file above to get started.<br>
                <span style="font-size:0.9rem; color:#6b7280;">
                    Required columns: <code>transaction_id</code>, 
                    <code>amount</code>, <code>account_age</code>, <code>location</code>
                </span>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Monitoring Log History (always visible) ──────────────────────────────────
st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

_log_path = os.path.join(PROJECT_ROOT, "logs", "monitoring_log.csv")
if os.path.isfile(_log_path):
    st.markdown(
        '<div class="glass-card"><h3>📋 Monitoring Log History</h3></div>',
        unsafe_allow_html=True,
    )
    _log_df = pd.read_csv(_log_path)
    st.dataframe(_log_df.tail(10), use_container_width=True, hide_index=True)

st.markdown(
    '<div class="glass-card" style="text-align:center; padding:1rem;">'
    '<p style="color:#9ca3af; font-size:0.95rem; margin:0;">'
    '📊 Logs are stored in <code>logs/monitoring_log.csv</code> and can be visualized in '
    '<strong>Tableau</strong> dashboards.</p></div>',
    unsafe_allow_html=True,
)
