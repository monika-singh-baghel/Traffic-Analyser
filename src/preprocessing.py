"""Functions for cleaning and preparing traffic data."""

import pandas as pd


def preprocess_traffic_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Convert dates, sort rows, and fill missing visitor values using interpolation."""
    processed_df = dataframe.copy()

    processed_df["Date"] = pd.to_datetime(processed_df["Date"], errors="coerce")
    if processed_df["Date"].isna().any():
        raise ValueError("The Date column contains invalid date values.")

    processed_df["Visitors"] = pd.to_numeric(processed_df["Visitors"], errors="coerce")

    processed_df = processed_df.sort_values("Date").reset_index(drop=True)

    if processed_df["Visitors"].isna().all():
        raise ValueError("The Visitors column does not contain any valid numeric values.")

    processed_df["Visitors"] = processed_df["Visitors"].interpolate(method="linear")
    processed_df["Visitors"] = processed_df["Visitors"].bfill().ffill()

    return processed_df
