
import pandas as pd
from pathlib import Path

DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "UNSW_NB15_training-set.csv"
)

def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)
    return df


def preprocess_data(df):
    df = df.copy()

    # Remove duplicate records
    df = df.drop_duplicates()

    # Handle missing attack categories
    if "attack_cat" in df.columns:
        df["attack_cat"] = (
            df["attack_cat"]
            .fillna("Unknown")
            .str.strip()
        )

    # Fill missing numerical values using median
    numeric_cols = df.select_dtypes(
        include="number"
    ).columns

    for col in numeric_cols:
        if df[col].isna().any():
            df[col] = df[col].fillna(
                df[col].median()
            )

    return df
