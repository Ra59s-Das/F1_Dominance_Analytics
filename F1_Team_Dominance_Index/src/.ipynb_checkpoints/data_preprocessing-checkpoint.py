"""
data_processing.py
----------------------
Handles loading, cleaning, and preprocessing Formula 1 datasets.
Generates a clean season-level summary for each constructor (team).
"""

import os
from pathlib import Path
import pandas as pd


def load_data(raw_data_dir):
    """Loads all CSV files from the raw data directory into a dictionary."""
    datasets = {}
    if not os.path.exists(raw_data_dir):
        raise FileNotFoundError(f"❌ Raw data directory not found: {raw_data_dir}")

    for file in os.listdir(raw_data_dir):
        if file.endswith(".csv"):
            name = file.replace(".csv", "")
            path = os.path.join(raw_data_dir, file)
            df = pd.read_csv(path)
            datasets[name] = df
            print(f"✅ Loaded {file} ({df.shape[0]} rows, {df.shape[1]} cols)")
    return datasets


def clean_column_names(df):
    """Standardize column names to lowercase and snake_case."""
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def preprocess_all(datasets):
    """
    Performs basic preprocessing and merges key datasets.
    Returns season-level team summary (year, team, races, wins, podiums, total points).
    """
    for key in datasets:
        datasets[key] = clean_column_names(datasets[key])

    races = datasets.get("races")
    results = datasets.get("results")
    constructors = datasets.get("constructors")
    standings = datasets.get("constructor_standings")

    # Merge race and team data
    merged = (
        results
        .merge(
            races[["raceid", "year", "name", "round"]],
            on="raceid",
            how="left"
        )
        .merge(
            constructors[["constructorid", "name"]].rename(columns={"name": "team"}),
            on="constructorid",
            how="left"
        )
    )

    # Season summary per team
    team_summary = (
        merged.groupby(["year", "team"])
        .agg(
            races=("raceid", "nunique"),
            wins=("positionorder", lambda x: (x == 1).sum()),
            podiums=("positionorder", lambda x: (x <= 3).sum()),
            total_points=("points", "sum"),
        )
        .reset_index()
    )

    # Merge with constructor standings for max points in a season
    if standings is not None:
        season_points = (
            standings.groupby(["year", "constructorid"])
            .agg(season_points=("points", "max"))
            .reset_index()
            .merge(
                constructors[["constructorid", "name"]].rename(columns={"name": "team"}),
                on="constructorid",
                how="left"
            )
        )
        team_summary = team_summary.merge(season_points, on=["year", "team"], how="left")

    print(f"✅ Preprocessed team summary: {team_summary.shape}")
    return team_summary


def save_processed_data(df, processed_dir, filename="team_year_summary.csv"):
    """Saves the preprocessed dataset to processed directory."""
    Path(processed_dir).mkdir(parents=True, exist_ok=True)
    path = os.path.join(processed_dir, filename)
    df.to_csv(path, index=False)
    print(f"💾 Saved processed data → {path}")


# Example run (if executed directly)
if __name__ == "__main__":
    RAW_DIR = "../data/raw"
    PROCESSED_DIR = "../data/processed"

    data = load_data(RAW_DIR)
    summary = preprocess_all(data)
    save_processed_data(summary, PROCESSED_DIR)
