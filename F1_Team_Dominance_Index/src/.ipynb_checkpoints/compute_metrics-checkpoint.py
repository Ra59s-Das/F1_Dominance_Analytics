"""
compute_metrics.py
-------------------
Compute additional team-season metrics for F1 Team Dominance Index (TDI).
"""

import os
import pandas as pd
from pathlib import Path

def load_processed_data(processed_dir, filename="team_year_summary.csv"):
    file_path = os.path.join(processed_dir, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    df = pd.read_csv(file_path)
    print(f"✅ Loaded: {filename} shape: {df.shape}")
    return df


def compute_additional_metrics(df):
    df = df.copy()
    
    df['total_races'] = df['races']

    df['points_share'] = df['total_points'] / df.groupby('year')['total_points'].transform('sum')

    if 'one_two_finishes' in df.columns:
        df['one_two_rate'] = df['one_two_finishes'] / df['total_races']
    else:
        df['one_two_rate'] = 0.0

    df['avg_points'] = df['total_points'] / df['total_races']

    return df


def save_metrics_data(df, processed_dir, filename="team_year_summary_with_metrics.csv"):
    Path(processed_dir).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(processed_dir, filename)
    df.to_csv(file_path, index=False)
    print(f"💾 Saved metrics-enhanced file to: {file_path}")


if __name__ == "__main__":
    PROCESSED_DIR = r"C:\Users\ASUS\OneDrive\Documents\Desktop\F1_Dominance_Analytics\F1_Team_Dominance_Index\data\processed"

    df = load_processed_data(PROCESSED_DIR, "team_year_summary.csv")
    df_metrics = compute_additional_metrics(df)

    save_metrics_data(df_metrics, PROCESSED_DIR)
