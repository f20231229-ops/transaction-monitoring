"""
generate_logs.py — Synthetic Monitoring Log Generator

Creates a realistic monitoring_log_sample.csv with smooth trends,
periodic anomaly spikes, and gradual drift episodes for Tableau demos.
"""

import csv
import math
import random
from datetime import datetime, timedelta

random.seed(42)

ROWS = 250
START_DATE = datetime(2025, 7, 1, 8, 0, 0)
OUTPUT_PATH = "data/monitoring_log_sample.csv"

COLUMNS = [
    "date",
    "total_transactions",
    "missing_percent",
    "anomaly_count",
    "drift_score",
    "alert",
]

DRIFT_ALERT_THRESHOLD = 20.0


def generate():
    rows = []

    for i in range(ROWS):
        ts = START_DATE + timedelta(hours=i * 6, minutes=random.randint(0, 59))

        # Base transaction count: 800-1200 with weekly seasonality
        base_txn = 1000 + int(150 * math.sin(2 * math.pi * i / 28))
        total_transactions = base_txn + random.randint(-50, 50)

        # Missing %: low baseline (~0.3-1.5) with occasional bumps
        missing_percent = round(random.gauss(0.8, 0.3), 2)
        if random.random() < 0.08:
            missing_percent = round(random.uniform(2.5, 5.0), 2)
        missing_percent = max(0.0, missing_percent)

        # Anomaly count: mostly 0-2, with periodic spikes
        anomaly_count = max(0, int(random.gauss(1, 0.8)))
        # Spike episodes around indices 60-70, 130-145, 200-215
        if 60 <= i <= 70 or 130 <= i <= 145 or 200 <= i <= 215:
            anomaly_count = random.randint(5, 18)
        elif random.random() < 0.05:
            anomaly_count = random.randint(3, 8)

        # Drift score: baseline 2-8%, with drift episodes
        drift_score = round(random.gauss(5, 2), 2)
        # Gradual drift rises around indices 80-100, 160-180
        if 80 <= i <= 100:
            drift_score = round(12 + (i - 80) * 1.2 + random.gauss(0, 2), 2)
        elif 160 <= i <= 180:
            drift_score = round(15 + (i - 160) * 1.5 + random.gauss(0, 3), 2)
        elif 200 <= i <= 215:
            drift_score = round(25 + random.gauss(0, 5), 2)
        drift_score = max(0.0, drift_score)

        # Alert logic
        has_anomaly = anomaly_count > 0
        has_drift = drift_score > DRIFT_ALERT_THRESHOLD

        if has_anomaly and has_drift:
            alert = "Anomaly + Drift"
        elif has_anomaly:
            alert = "Anomaly Detected"
        elif has_drift:
            alert = "Drift Detected"
        else:
            alert = "Healthy"

        rows.append({
            "date": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "total_transactions": total_transactions,
            "missing_percent": missing_percent,
            "anomaly_count": anomaly_count,
            "drift_score": drift_score,
            "alert": alert,
        })

    with open(OUTPUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows → {OUTPUT_PATH}")

    # Quick stats
    alerts = [r for r in rows if r["alert"] != "Healthy"]
    print(f"  Alert rows: {len(alerts)}/{len(rows)}")
    print(f"  Max anomaly_count: {max(r['anomaly_count'] for r in rows)}")
    print(f"  Max drift_score: {max(r['drift_score'] for r in rows)}")
    print(f"  Date range: {rows[0]['date']} → {rows[-1]['date']}")


if __name__ == "__main__":
    generate()
