"""Functions for loading website traffic data."""

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {"Date", "Visitors"}


def load_traffic_data(file_source) -> pd.DataFrame:
    """Load traffic data from a CSV file and validate its structure."""
    try:
        dataframe = pd.read_csv(file_source)
    except Exception as error:
        raise ValueError(f"Unable to read the CSV file: {error}") from error

    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"CSV file is missing required columns: {missing}")

    return dataframe.copy()


def load_default_data() -> pd.DataFrame:
    """Load the sample dataset stored in the project's data folder."""
    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "data" / "traffic.csv"
    return load_traffic_data(data_path)
