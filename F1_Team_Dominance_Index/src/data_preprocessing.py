"""
data_processing.py
-------------------
Handles loading, cleaning, and preparing team-season level Formula 1 data
for the Team Dominance Index (TDI) pipeline.

Input:
    ../data/raw/ (optional)
    ../data/processed/*.csv

Output:
    Cleaned and validated DataFrames for downstream processing.
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

def load_processed_data(processed_dir: str = PROCESSED_DIR):
   
    if not os.path.exists(processed_dir):
        raise FileNotFoundError(f"Processed data directory not found: {processed_dir}")

    print(f"📂 Processed folder: {os.path.abspath(processed_dir)}")
    csv_files = [f for f in os.listdir(processed_dir) if f.endswith(".csv")]
    if not csv_files:
        raise FileNotFoundError(" No CSV files found in processed data folder.")

    print(" CSV files found in data/processed:")
    for file in csv_files:
        print(f" - {file}")

    data_dict = {}
    for file in csv_files:
        path = os.path.join(processed_dir, file)
        df = pd.read_csv(path)
        data_dict[file.replace(".csv", "")] = df

    return data_dict


def clean_dataframe(df: pd.DataFrame, name: str):
    
    print(f"\n🧹 Cleaning: {name}")

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Drop duplicates
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    if before != after:
        print(f"Removed {before - after} duplicate rows.")

    # Null check
    null_counts = df.isnull().sum()
    null_cols = null_counts[null_counts > 0]
    if not null_cols.empty:
        print("Columns with missing values:")
        print(null_cols)
    else:
        print("No missing values found.")

    print(f"Shape after cleaning: {df.shape}")
    return df


def prepare_datasets():
   
    datasets = load_processed_data(PROCESSED_DIR)

    team_summary = datasets.get("team_year_summary")
    team_dominance = datasets.get("team_dominance_index_with_alt")

    if team_summary is None or team_dominance is None:
        raise KeyError("Required datasets not found. Ensure processed files exist.")

    team_summary = clean_dataframe(team_summary, "team_year_summary")
    team_dominance = clean_dataframe(team_dominance, "team_dominance_index_with_alt")

    print("\n✅ All datasets loaded and cleaned successfully.\n")
    return team_summary, team_dominance


if __name__ == "__main__":
    try:
        team_summary, team_dominance = prepare_datasets()

        print("\n=== team_year_summary (sample) ===")
        print(team_summary.head(5))

        print("\n=== team_dominance_index_with_alt (sample) ===")
        print(team_dominance.head(5))

    except Exception as e:
        print(f"\n Error: {e}")
