"""
logger.py — Monitoring Log Writer

Appends a single-row summary of each pipeline run to logs/monitoring_log.csv.
The CSV is formatted for direct consumption by Tableau.
"""

import os
import csv
from datetime import datetime

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LOG_PATH = os.path.join(_THIS_DIR, "..", "logs", "monitoring_log.csv")

LOG_COLUMNS = [
    "date",
    "total_transactions",
    "missing_percent",
    "anomaly_count",
    "drift_score",
    "alert",
]

DRIFT_ALERT_THRESHOLD = 20.0  # percent


def log_results(results: dict, log_path: str = DEFAULT_LOG_PATH) -> str:
    """
    Append one summary row to the monitoring log CSV.

    Parameters
    ----------
    results : dict — must contain keys:
        total_transactions, missing_percent, anomaly_count, drift_score
    log_path : str — path to the CSV file

    Returns
    -------
    str — alert status label for Tableau:
        "Healthy", "Anomaly Detected", "Drift Detected", or "Anomaly + Drift"
    """
    has_anomaly = results["anomaly_count"] > 0
    has_drift = results["drift_score"] > DRIFT_ALERT_THRESHOLD

    if has_anomaly and has_drift:
        alert = "Anomaly + Drift"
    elif has_anomaly:
        alert = "Anomaly Detected"
    elif has_drift:
        alert = "Drift Detected"
    else:
        alert = "Healthy"

    row = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_transactions": int(results["total_transactions"]),
        "missing_percent": float(results["missing_percent"]),
        "anomaly_count": int(results["anomaly_count"]),
        "drift_score": float(results["drift_score"]),
        "alert": alert,
    }

    file_exists = os.path.isfile(log_path)

    with open(log_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_COLUMNS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    return alert
