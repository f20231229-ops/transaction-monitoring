"""
drift.py — Distribution Drift Scoring

Compares the mean transaction amount of uploaded data against a stored baseline.
"""

import os
import pandas as pd

# Resolve baseline path relative to this file's location
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BASELINE_PATH = os.path.join(_THIS_DIR, "..", "data", "baseline.csv")


def calculate_drift(
    uploaded_df: pd.DataFrame,
    baseline_path: str = DEFAULT_BASELINE_PATH,
) -> dict:
    """
    Calculate drift between the uploaded dataset and the baseline.

    Returns
    -------
    dict with keys:
        baseline_mean : float — mean amount in baseline
        uploaded_mean : float — mean amount in uploaded data
        drift_score   : float — absolute % change
    """
    baseline_df = pd.read_csv(baseline_path)
    baseline_mean = float(baseline_df["amount"].mean())
    uploaded_mean = float(uploaded_df["amount"].mean())

    if baseline_mean == 0:
        drift_score = 0.0
    else:
        drift_score = round(abs(uploaded_mean - baseline_mean) / abs(baseline_mean) * 100, 2)

    return {
        "baseline_mean": round(baseline_mean, 2),
        "uploaded_mean": round(uploaded_mean, 2),
        "drift_score": drift_score,
    }
