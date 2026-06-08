"""
anomaly.py — Rule-Based Anomaly Detection

Flags transactions where the amount is suspiciously high relative to account age.
Rule:  amount > 5000  AND  account_age < 30 days
"""

import pandas as pd

AMOUNT_THRESHOLD = 5000
AGE_THRESHOLD = 30  # days


def detect_anomalies(df: pd.DataFrame) -> dict:
    """
    Detect anomalous transactions using a rule-based approach.

    Returns
    -------
    dict with keys:
        anomaly_count : int           — number of flagged rows
        anomaly_rows  : pd.DataFrame  — subset of flagged rows
    """
    mask = (df["amount"] > AMOUNT_THRESHOLD) & (df["account_age"] < AGE_THRESHOLD)
    anomaly_rows = df[mask].copy()

    return {
        "anomaly_count": len(anomaly_rows),
        "anomaly_rows": anomaly_rows,
    }
