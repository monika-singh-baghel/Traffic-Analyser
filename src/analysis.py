"""Functions for traffic trend analysis and simple forecasting."""

from __future__ import annotations

from typing import Tuple

import pandas as pd


def calculate_moving_average(dataframe: pd.DataFrame, window: int = 3) -> pd.DataFrame:
    """Add a moving average trend column to the processed traffic data."""
    analyzed_df = dataframe.copy()
    analyzed_df["Trend"] = analyzed_df["Visitors"].rolling(window=window, min_periods=1).mean()
    return analyzed_df


def predict_future_traffic(dataframe: pd.DataFrame, days: int = 5) -> pd.DataFrame:
    """Predict future traffic using the latest trend change between recent values."""
    if dataframe.empty:
        raise ValueError("Cannot predict future traffic from an empty dataset.")

    last_date = dataframe["Date"].iloc[-1]
    last_value = float(dataframe["Visitors"].iloc[-1])

    if len(dataframe) >= 2:
        recent_change = float(dataframe["Visitors"].iloc[-1] - dataframe["Visitors"].iloc[-2])
    else:
        recent_change = 0.0

    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=days, freq="D")
    predictions = []

    current_value = last_value
    for _ in range(days):
        current_value = max(0.0, current_value + recent_change)
        predictions.append(round(current_value, 2))

    return pd.DataFrame({"Date": future_dates, "Predicted Visitors": predictions})


def analyze_traffic(dataframe: pd.DataFrame, window: int = 3, future_days: int = 5) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Run moving average analysis and future prediction together."""
    analyzed_df = calculate_moving_average(dataframe, window=window)
    future_df = predict_future_traffic(analyzed_df, days=future_days)
    return analyzed_df, future_df
