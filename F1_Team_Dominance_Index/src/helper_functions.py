import pandas as pd
import numpy as np
import os
import logging

# ------------------------------------------------------
# Logging Setup
# ------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

# ------------------------------------------------------
# File Helpers
# ------------------------------------------------------
def load_csv(path):
    if not os.path.exists(path):
        logging.error(f"File not found: {path}")
        return None
    try:
        df = pd.read_csv(path)
        logging.info(f"Loaded file: {path}  | Shape: {df.shape}")
        return df
    except Exception as e:
        logging.error(f"Error reading CSV {path}: {e}")
        return None


def save_csv(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    logging.info(f"Saved file: {path}  | Shape: {df.shape}")

# ------------------------------------------------------
# Math Helpers
# ------------------------------------------------------
def safe_div(a, b):
    return a / b if b != 0 else 0


def normalize(series):
    return (series - series.min()) / (series.max() - series.min() + 1e-9)

# ------------------------------------------------------
# Folder Helpers
# ------------------------------------------------------
def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    logging.info(f"Ensured directory exists: {path}")
