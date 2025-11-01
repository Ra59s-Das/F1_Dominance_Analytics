"""
data_preprocessing.py
----------------------
This module loads and preprocesses Formula 1 datasets to create
a clean, season-level summary for each constructor (team).
"""

import os
import pandas as pd
from pathlib import Path

def load_data(raw_data_dir):
    """Loads all CSVs from the raw data directory."""
    datasets = {}
    for file in os.listdir(raw_data_dir):
        if file.endswith(".csv"):
            name = file.replace(".csv", "")
            datasets[name] = pd.read_csv(os.path.join(raw_data_dir, file))
            print(f"✅ Loaded {file} ({datasets[name].shape[0]} rows)")
    return datasets


def clean_column_names(df):
    """Standardizes column names to lowercase and snake_case."""
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def preprocess_all(datasets):
    """Basic preprocessing for key F1 datasets."""
    # Clean column names
    for key in datasets:
        datasets[key] = clean_column_names(datasets[key])

    # Merge key datasets
    races = datasets.get("races")
    results = datasets.get("results")
    constructors = datasets.get("constructors")
    standings = datasets.get("constructor_standings")

    merged = (
        results
        .merge(races[["raceid", "year", "name", "round"]], on="raceid", how="left")
        .merge(constructors[["constructorid", "name"]].rename(columns={"name": "team"}), on="constructorid", how="left")
    )

    # Compute season-level summary
    team_summary = (
        merged.groupby(["year", "team"])
        .agg(
            total_races=("raceid", "nunique"),
            wins=("positionorder", lambda x: (x == 1).sum()),
            podiums=("positionorder", lambda x: (x <= 3).sum()),
            total_points=("points", "sum"),
        )
        .reset_index()
    )

    # Merge with constructor standings for total season points
    if standings is not None:
        season_points = (
            standings.groupby(["year", "constructorid"])
            .agg(season_points=("points", "max"))
            .reset_index()
            .merge(constructors[["constructorid", "name"]].rename(columns={"name": "team"}), on="constructorid", how="left")
        )
        team_summary = team_summary.merge(season_points, on=["year", "team"], how="left")

    return team_summary


def save_processed_data(df, processed_dir, filename="team_year_summary.csv"):
    """Saves cleaned dataset to processed folder."""
    Path(processed_dir).mkdir(parents=True, exist_ok=True)
    output_path = os.path.join(processed_dir, filename)
    df.to_csv(output_path, index=False)
    print(f"💾 Saved processed file: {output_path}")
