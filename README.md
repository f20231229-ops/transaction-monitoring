# 🛡️ Transaction Data Monitoring & Alerting System

A production-style data monitoring pipeline that detects anomalies, measures distribution drift, and generates Tableau-ready alert logs — all through a polished Streamlit interface.

---

## ✨ Features

- **CSV Upload Interface** — Drag-and-drop transaction data via Streamlit
- **Data Quality Checks** — Flags missing values and negative amounts
- **Anomaly Detection** — Rule-based engine (high amount + low account age)
- **Drift Detection** — Compares uploaded data distribution against a stored baseline
- **Automated Logging** — Appends structured results to a Tableau-compatible CSV
- **Alert Classification** — `Healthy` · `Anomaly Detected` · `Drift Detected` · `Anomaly + Drift`

---

## 🏗️ Architecture

```
┌──────────────┐     ┌──────────────────────────────────────────┐     ┌──────────────┐
│  CSV Upload  │────▶│           Monitoring Pipeline            │────▶│  Tableau CSV  │
│  (Streamlit) │     │  checks → anomaly → drift → logger      │     │  Dashboard    │
└──────────────┘     └──────────────────────────────────────────┘     └──────────────┘
```

---

## 📂 Project Structure

```
transaction-monitoring/
│
├── data/
│   ├── baseline.csv                  # Reference dataset for drift comparison
│   ├── test_upload.csv               # Sample upload file (triggers alerts)
│   └── monitoring_log_sample.csv     # Pre-generated sample log for Tableau
│
├── src/
│   ├── checks.py                     # Data quality checks
│   ├── anomaly.py                    # Rule-based anomaly detection
│   ├── drift.py                      # Distribution drift scoring
│   ├── logger.py                     # Append results to monitoring_log.csv
│   └── pipeline.py                   # Master pipeline orchestrator
│
├── dashboard/
│   └── app.py                        # Streamlit web interface
│
├── assets/
│   ├── ui.png                        # Streamlit dashboard screenshot
│   └── tableau.png                   # Tableau dashboard screenshot
│
├── generate_logs.py                  # Synthetic monitoring log generator
├── requirements.txt                  # Python dependencies
├── .gitignore
└── README.md
```

---

## 🚀 How to Run

```bash
# Clone the repository
git clone https://github.com/<your-username>/transaction-monitoring.git
cd transaction-monitoring

# Install dependencies
pip install -r requirements.txt

# Launch the dashboard
streamlit run dashboard/app.py
```

Then upload `data/test_upload.csv` to see the full pipeline in action.

---

## 📊 Monitoring Rules

| Check | Rule | Threshold |
|-------|------|-----------|
| Missing Data | % of null cells across all columns | Reported as metric |
| Anomaly | `amount > 5000` AND `account_age < 30` | Flagged per row |
| Drift | Absolute % change in mean `amount` vs baseline | Alert if > 20% |

---

## 📈 Tableau Integration

The pipeline outputs `logs/monitoring_log.csv` with clean, flat columns optimized for Tableau:

| Column | Type | Description |
|--------|------|-------------|
| `date` | datetime | Pipeline run timestamp |
| `total_transactions` | int | Row count per run |
| `missing_percent` | float | % of null cells |
| `anomaly_count` | int | Flagged transaction count |
| `drift_score` | float | % deviation from baseline |
| `alert` | string | `Healthy` / `Anomaly Detected` / `Drift Detected` / `Anomaly + Drift` |

### Setting Up in Tableau

1. **Connect** → Text file → select `logs/monitoring_log.csv` (or use the sample at `data/monitoring_log_sample.csv`)
2. **Create charts:**
   - Line chart: `anomaly_count` vs `date`
   - Area chart: `drift_score` vs `date` (add reference line at 20%)
   - Bar chart: `missing_percent` vs `date`
   - Highlight table: alert status with color-coded labels
3. **Combine** all worksheets into a single dashboard with a date filter

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Pandas** — Data manipulation
- **NumPy** — Numerical operations
- **Streamlit** — Web interface
- **Tableau** — Reporting & visualization

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
