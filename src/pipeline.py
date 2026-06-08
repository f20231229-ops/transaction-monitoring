"""
pipeline.py — Master Monitoring Pipeline

Orchestrates all monitoring steps and returns a consolidated results dict.
"""

import pandas as pd

from src.checks import run_quality_checks
from src.anomaly import detect_anomalies
from src.drift import calculate_drift
from src.logger import log_results


def run_monitoring_pipeline(uploaded_df: pd.DataFrame) -> dict:
    """
    Execute the full monitoring pipeline on an uploaded DataFrame.

    Steps
    -----
    1. Data quality checks  (missing %, negative amounts)
    2. Anomaly detection    (high amount + low account age)
    3. Drift scoring        (mean amount vs baseline)
    4. Log results          (append to monitoring_log.csv)

    Returns
    -------
    dict with all results merged plus an 'alert' flag.
    """
    # Ensure numeric columns are properly typed (handles blanks / mixed CSVs)
    uploaded_df = uploaded_df.copy()
    uploaded_df["amount"] = pd.to_numeric(uploaded_df["amount"], errors="coerce")
    if "account_age" in uploaded_df.columns:
        uploaded_df["account_age"] = pd.to_numeric(uploaded_df["account_age"], errors="coerce")

    # Step 1: Quality checks
    quality = run_quality_checks(uploaded_df)

    # Step 2: Anomaly detection
    anomalies = detect_anomalies(uploaded_df)

    # Step 3: Drift scoring
    drift = calculate_drift(uploaded_df)

    # Consolidate results
    results = {
        "total_transactions": len(uploaded_df),
        "missing_percent": quality["missing_percent"],
        "negative_amount_count": quality["negative_amount_count"],
        "anomaly_count": anomalies["anomaly_count"],
        "anomaly_rows": anomalies["anomaly_rows"],
        "baseline_mean": drift["baseline_mean"],
        "uploaded_mean": drift["uploaded_mean"],
        "drift_score": drift["drift_score"],
    }

    # Step 4: Log and get alert flag
    alert = log_results(results)
    results["alert"] = alert

    return results
