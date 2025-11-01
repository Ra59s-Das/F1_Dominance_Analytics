import pandas as pd

def load_raw_data():
    """Loads raw datasets from Data/raw folder."""
    races = pd.read_csv("../Data/raw/races.csv")
    results = pd.read_csv("../Data/raw/results.csv")
    drivers = pd.read_csv("../Data/raw/drivers.csv")
    constructors = pd.read_csv("../Data/raw/constructors.csv")
    return races, results, drivers, constructors

def clean_results(results):
    """Basic cleaning on results dataset."""
    results = results.dropna(subset=["positionOrder"])
    results["positionOrder"] = results["positionOrder"].astype(int)
    return results

def merge_datasets(races, results, drivers, constructors):
    """Merges races, results, drivers, and constructors data."""
    df = results.merge(races, on="raceId", how="left")
    df = df.merge(drivers, on="driverId", how="left")
    df = df.merge(constructors, on="constructorId", how="left")
    return df
