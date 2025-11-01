"""
helper_functions.py
--------------------
Utility functions for Formula 1 dominance analysis.
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def normalize_columns(df, columns):
    """Normalize numeric columns between 0 and 1."""
    scaler = MinMaxScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df


def calculate_tdi(df, weights=None):
    """Compute Team Dominance Index (TDI) using weighted metrics."""
    if weights is None:
        weights = {
            "win_rate": 0.35,
            "podium_rate": 0.25,
            "points_share": 0.20,
            "avg_qual_gap_inv": 0.15,
            "one_two_rate": 0.05,
        }

    # Weighted sum
    df["TDI"] = (
        df["win_rate"] * weights["win_rate"]
        + df["podium_rate"] * weights["podium_rate"]
        + df["points_share"] * weights["points_share"]
        + df["avg_qual_gap_inv"] * weights["avg_qual_gap_inv"]
        + df["one_two_rate"] * weights["one_two_rate"]
    )
    return df


def compute_rates(df):
    """Compute win_rate, podium_rate, etc."""
    df["win_rate"] = df["wins"] / df["total_races"]
    df["podium_rate"] = df["podiums"] / df["total_races"]
    df["points_share"] = df["total_points"] / df.groupby("year")["total_points"].transform("sum")
    return df
