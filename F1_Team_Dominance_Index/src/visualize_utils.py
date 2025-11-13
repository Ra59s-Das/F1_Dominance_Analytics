"""
visualize_utils.py
-------------------
Visualization utilities for Final Team Dominance Index dataset.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")


# ---------------------------------------------------------
# Load CSV
# ---------------------------------------------------------
def load_csv(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    df = pd.read_csv(path)
    print(f"Loaded: {path} → {df.shape[0]} rows, {df.shape[1]} columns")
    return df


# ---------------------------------------------------------
# Plot 1: Top N teams for a given year
# ---------------------------------------------------------
def plot_top_teams_by_year(df, year, top_n=10):
    df_year = df[df["year"] == year].sort_values("TDI", ascending=False).head(top_n)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_year, x="TDI", y="name")
    plt.title(f"Top {top_n} Teams by TDI in {year}")
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
# Plot 2: Team trends
# ---------------------------------------------------------
def plot_team_trends(df, teams):
    df_teams = df[df["name"].isin(teams)]

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_teams, x="year", y="TDI", hue="name", marker="o")
    plt.title("TDI Trends Over Years")
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
# Plot 3: TDI vs TDI_normalized
# ---------------------------------------------------------
def plot_tdi_vs_normalized(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="TDI", y="TDI_normalized", alpha=0.7)
    plt.title("TDI vs Normalized TDI")
    plt.tight_layout()
    plt.show()



# ---------------------------------------------------------
# Plot 4: Heatmap of dominance (Top N teams)
# ---------------------------------------------------------
def plot_tdi_heatmap(df, top_n=10):
    top_teams = (
        df.groupby("name")["TDI"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
        .index
    )

    df_top = df[df["name"].isin(top_teams)]

    pivot = df_top.pivot_table(
        values="TDI",
        index="name",
        columns="year",
        aggfunc="mean"
    )

    plt.figure(figsize=(16, 6))
    sns.heatmap(pivot, cmap="viridis")
    plt.title(f"Top {top_n} Team Dominance Heatmap (TDI)")
    plt.tight_layout()
    plt.show()



# ---------------------------------------------------------
# Plot 5: Dominance share pie chart for a given season
# ---------------------------------------------------------
def plot_dominance_pie(df, year, top_n=5):
    df_year = (
        df[df["year"] == year]
        .sort_values("TDI", ascending=False)
        .head(top_n)
    )

    plt.figure(figsize=(8, 8))
    plt.pie(
        df_year["TDI"],
        labels=df_year["name"],
        autopct="%1.1f%%",
        startangle=140
    )
    plt.title(f"Dominance Share ({year}) – Top {top_n} Teams")
    plt.tight_layout()
    plt.show()

# ---------------------------------------------------------
# Plot 6: Dominance trends for LAST 10 YEARS only (WITH LEGEND)
# ---------------------------------------------------------
def plot_last_10_years_dominance(df):
    last_year = df["year"].max()
    start_year = last_year - 9 

    df_last10 = df[df["year"].between(start_year, last_year)]

    plt.figure(figsize=(16, 7))

    for team in df_last10["name"].unique():
        subset = df_last10[df_last10["name"] == team]

        if len(subset) > 0:
            plt.plot(
                subset["year"],
                subset["TDI_normalized"],
                linewidth=2,
                alpha=0.8,
                label=team 
            )

    plt.title(f"F1 Team Dominance (Last 10 Years: {start_year}–{last_year})")
    plt.xlabel("Year")
    plt.ylabel("Normalized TDI")
    plt.grid(True, alpha=0.3)

    plt.legend(
        title="Teams",
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        borderaxespad=0,
        fontsize=9
    )

    plt.tight_layout()
    plt.show()





if __name__ == "__main__":
    print("🚀 Running visualize_utils.py...")

    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "../output/results/final_team_tdi.csv")

    try:
        df = load_csv(csv_path)

        # Plot 1
        plot_top_teams_by_year(df, year=2022)

        # Plot 2
        teams = ["Ferrari", "McLaren", "Mercedes", "Red Bull", "Williams"]
        plot_team_trends(df, teams)

        # Plot 3
        plot_tdi_vs_normalized(df)

        # Plot 4
        plot_tdi_heatmap(df, top_n=12)

        # Plot 5
        plot_dominance_pie(df, year=2022, top_n=6)

        # Plot 6 (NEW – Last 10 years only)
        plot_last_10_years_dominance(df)


        print("✅ All visualizations generated successfully.")

    except Exception as e:
        print("❌ Error:", e)
