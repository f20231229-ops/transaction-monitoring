"""
checks.py — Data Quality Checks

Calculates missing-value percentages and flags negative transaction amounts.
"""

import pandas as pd


def run_quality_checks(df: pd.DataFrame) -> dict:
    """
    Run basic data quality checks on the uploaded transaction DataFrame.

    Returns
    -------
    dict with keys:
        missing_percent    : float  — overall % of null cells
        negative_amount_count : int — rows where amount < 0
        negative_amount_rows  : list[int] — indices of those rows
    """
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isnull().sum().sum()
    missing_percent = round((missing_cells / total_cells) * 100, 2) if total_cells > 0 else 0.0

    negative_mask = df["amount"] < 0
    negative_amount_count = int(negative_mask.sum())
    negative_amount_rows = df.index[negative_mask].tolist()

    return {
        "missing_percent": missing_percent,
        "negative_amount_count": negative_amount_count,
        "negative_amount_rows": negative_amount_rows,
    }
