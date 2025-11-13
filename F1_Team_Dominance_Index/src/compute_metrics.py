"""
compute_metrics.py
-------------------
All metric calculations for the F1 Team Dominance Index (TDI) project.

This file:
- Computes win %, podium %, points share
- Computes normalized values
- Computes TDI and Alternate TDI
- Adds extra season-level metrics
"""

import pandas as pd
import numpy as np

# -----------------------------------------------------------
# 1. Compute additional raw metrics (win %, podium %, points share)
# -----------------------------------------------------------

def compute_additional_metrics(df):
    """
    Adds core percentage-based metrics for dominance:
    - win_rate
    - podium_rate
    - points_share
    - one_two_finish_rate (optional)
    """
    df = df.copy()

    # Avoid division errors
    df['total_races'] = df['total_races'].replace(0, np.nan)

    df['win_rate'] = df['wins'] / df['total_races']
    df['podium_rate'] = df['podiums'] / df['total_races']
    df['points_share'] = df['points'] / df.groupby('year')['points'].transform('sum')

    # Optional 1–2 finish metric if column exists
    if 'one_two_finishes' in df.columns:
        df['one_two_rate'] = df['one_two_finishes'] / df['total_races']
    else:
        df['one_two_rate'] = 0

    df = df.fillna(0)
    return df

# -----------------------------------------------------------
# 2. Normalize metrics (Min–Max Scaling)
# -----------------------------------------------------------

def normalize_metrics(df, metric_columns):
    """
    Applies Min-Max scaling to selected metrics within each season.
    """
    df = df.copy()

    for metric in metric_columns:
        df[f"{metric}_norm"] = df.groupby('year')[metric].transform(
            lambda x: (x - x.min()) / (x.max() - x.min()) if x.max() != x.min() else 1
        )

    return df

# -----------------------------------------------------------
# 3. Compute the Team Dominance Index (TDI)
# -----------------------------------------------------------

def compute_TDI(df):
    """
    Combines normalized metrics into one score: TDI
    Formula (example):
    TDI = 0.35 * win_norm + 0.25 * podium_norm + 0.25 * points_norm + 0.15 * one_two_norm
    """
    df = df.copy()

    df['TDI'] = (
        0.35 * df['win_rate_norm'] +
        0.25 * df['podium_rate_norm'] +
        0.25 * df['points_share_norm'] +
        0.15 * df['one_two_rate_norm']
    )

    return df

# -----------------------------------------------------------
# 4. Compute Alternate TDI (TDI_alt)
# -----------------------------------------------------------

def compute_TDI_alt(df):
    """
    Alternate version (more weight to points share).
    Useful for sensitivity analysis.
    """
    df = df.copy()

    df['TDI_alt'] = (
        0.25 * df['win_rate_norm'] +
        0.15 * df['podium_rate_norm'] +
        0.45 * df['points_share_norm'] +
        0.15 * df['one_two_rate_norm']
    )

    return df

# -----------------------------------------------------------
# 5. Master function to compute all metrics
# -----------------------------------------------------------

def build_all_metrics(df):
    """
    Combines all functions:
    1. Add raw metrics
    2. Normalize
    3. Compute TDI & alternate TDI
    """
    df = compute_additional_metrics(df)

    normalize_cols = ['win_rate', 'podium_rate', 'points_share', 'one_two_rate']
    df = normalize_metrics(df, normalize_cols)

    df = compute_TDI(df)
    df = compute_TDI_alt(df)

    return df

# -----------------------------------------------------------
# 6. Script mode (if someone runs this file alone)
# -----------------------------------------------------------

if __name__ == "__main__":
    print("⚙ compute_metrics.py should not be run directly.")
    print("Import functions inside your notebooks or main_pipeline.py.")
