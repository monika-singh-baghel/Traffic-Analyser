"""Functions for plotting traffic trends."""

import matplotlib.pyplot as plt
import pandas as pd


def create_traffic_plot(dataframe: pd.DataFrame):
    """Create a matplotlib figure for actual visitors and the moving average trend."""
    plt.style.use("seaborn-v0_8-whitegrid")
    figure, axis = plt.subplots(figsize=(11, 5.5))
    figure.patch.set_facecolor("#f9fcfa")
    axis.set_facecolor("#f9fcfa")

    axis.plot(
        dataframe["Date"],
        dataframe["Visitors"],
        marker="o",
        linewidth=2.4,
        markersize=6,
        color="#0c8a73",
        label="Actual Visitors",
    )
    axis.plot(
        dataframe["Date"],
        dataframe["Trend"],
        linestyle="--",
        linewidth=2.6,
        color="#143d73",
        label="Trend Line",
    )

    axis.fill_between(
        dataframe["Date"],
        dataframe["Visitors"],
        dataframe["Trend"],
        color="#bfe9df",
        alpha=0.22,
    )

    axis.set_title("Website Traffic Trend Analysis", fontsize=15, fontweight="bold", color="#17322c")
    axis.set_xlabel("Date")
    axis.set_ylabel("Visitors")
    axis.legend(frameon=False, loc="upper left")
    axis.grid(True, linestyle="--", alpha=0.25)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["left"].set_alpha(0.2)
    axis.spines["bottom"].set_alpha(0.2)
    figure.autofmt_xdate()
    figure.tight_layout()

    return figure
