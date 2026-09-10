"""Streamlit app for the Web Traffic Trend Analyzer project."""

import pandas as pd
import streamlit as st

from src.analysis import analyze_traffic
from src.data_loader import load_default_data, load_traffic_data
from src.preprocessing import preprocess_traffic_data
from src.visualization import create_traffic_plot


st.set_page_config(
    page_title="Web Traffic Trend Analyzer",
    page_icon="📈",
    layout="wide",
)


def apply_custom_css() -> None:
    """Inject custom styling for a more polished dashboard layout."""
    st.markdown(
        """
        <style>
            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(0, 196, 140, 0.18), transparent 30%),
                    radial-gradient(circle at top right, rgba(20, 64, 133, 0.18), transparent 28%),
                    linear-gradient(180deg, #f4f7f2 0%, #edf3ee 100%);
                color: #17322c;
            }

            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }

            .hero {
                padding: 2rem 2.2rem;
                border-radius: 24px;
                background: linear-gradient(135deg, #0c5f52 0%, #143d73 100%);
                color: #f8fff9;
                box-shadow: 0 20px 45px rgba(16, 46, 68, 0.18);
                margin-bottom: 1.25rem;
            }

            .hero h1 {
                margin: 0;
                font-size: 2.4rem;
                line-height: 1.1;
            }

            .hero p {
                margin: 0.75rem 0 0;
                max-width: 760px;
                font-size: 1rem;
                opacity: 0.92;
            }

            .section-card {
                background: rgba(255, 255, 255, 0.78);
                border: 1px solid rgba(12, 95, 82, 0.10);
                border-radius: 20px;
                padding: 1.1rem 1.15rem;
                box-shadow: 0 12px 30px rgba(23, 50, 44, 0.08);
                backdrop-filter: blur(8px);
                margin-bottom: 1rem;
            }

            .metric-card {
                background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(240,247,243,0.88));
                border: 1px solid rgba(12, 95, 82, 0.10);
                border-radius: 18px;
                padding: 1rem 1.1rem;
                box-shadow: 0 10px 24px rgba(23, 50, 44, 0.07);
            }

            .metric-label {
                font-size: 0.88rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: #4f6f68;
                margin-bottom: 0.3rem;
            }

            .metric-value {
                font-size: 1.75rem;
                font-weight: 700;
                color: #143d73;
                line-height: 1.1;
            }

            .metric-delta {
                margin-top: 0.35rem;
                color: #0c5f52;
                font-size: 0.92rem;
            }

            [data-testid="stSidebar"] {
                background: rgba(248, 252, 249, 0.92);
                border-right: 1px solid rgba(12, 95, 82, 0.08);
            }

            div[data-testid="stDataFrame"] {
                border-radius: 16px;
                overflow: hidden;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label: str, value: str, delta: str) -> None:
    """Render a styled metric summary card."""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-delta">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    """Run the Streamlit web interface."""
    apply_custom_css()

    st.markdown(
        """
        <div class="hero">
            <h1>Web Traffic Trend Analyzer</h1>
            <p>
                Explore visitor patterns with a cleaner dashboard, interactive controls, and a quick
                forecast view. Upload your own CSV or use the included sample dataset to get started.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.header("Controls")
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
        moving_window = st.slider("Trend window", min_value=2, max_value=14, value=3)
        forecast_days = st.slider("Forecast days", min_value=3, max_value=30, value=5)
        show_raw_data = st.toggle("Show raw data table", value=False)
        show_processed_data = st.toggle("Show processed data table", value=True)

    try:
        if uploaded_file is not None:
            raw_df = load_traffic_data(uploaded_file)
            source_name = uploaded_file.name
        else:
            raw_df = load_default_data()
            source_name = "sample dataset (data/traffic.csv)"

        processed_df = preprocess_traffic_data(raw_df)

        min_date = processed_df["Date"].min().date()
        max_date = processed_df["Date"].max().date()

        with st.sidebar:
            selected_range = st.date_input(
                "Date range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
            )

        if len(selected_range) == 2:
            start_date, end_date = selected_range
        else:
            start_date, end_date = min_date, max_date

        filtered_df = processed_df[
            processed_df["Date"].between(pd.Timestamp(start_date), pd.Timestamp(end_date))
        ].copy()

        if filtered_df.empty:
            st.warning("No rows match the selected date range. Adjust the filter to continue.")
            return

        analyzed_df, future_df = analyze_traffic(
            filtered_df,
            window=moving_window,
            future_days=forecast_days,
        )

        total_visitors = int(round(analyzed_df["Visitors"].sum()))
        avg_visitors = analyzed_df["Visitors"].mean()
        peak_row = analyzed_df.loc[analyzed_df["Visitors"].idxmax()]
        first_value = analyzed_df["Visitors"].iloc[0]
        last_value = analyzed_df["Visitors"].iloc[-1]
        change_pct = 0.0 if first_value == 0 else ((last_value - first_value) / first_value) * 100

        metric_cols = st.columns(4)
        with metric_cols[0]:
            render_metric_card("Data Source", source_name, f"{len(analyzed_df)} records in view")
        with metric_cols[1]:
            render_metric_card("Total Visitors", f"{total_visitors:,}", f"Average {avg_visitors:.1f} per day")
        with metric_cols[2]:
            render_metric_card(
                "Peak Day",
                peak_row["Date"].strftime("%d %b %Y"),
                f"{peak_row['Visitors']:.0f} visitors",
            )
        with metric_cols[3]:
            render_metric_card("Period Change", f"{change_pct:+.1f}%", f"From {first_value:.0f} to {last_value:.0f}")

        overview_col, forecast_col = st.columns([2.2, 1])

        with overview_col:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("Traffic Visualization")
            st.caption(
                f"Trend line uses a {moving_window}-day moving average across "
                f"{start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')}."
            )
            chart = create_traffic_plot(analyzed_df)
            st.pyplot(chart, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with forecast_col:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("Forecast Snapshot")
            st.caption(f"Projected traffic for the next {forecast_days} day(s).")
            st.dataframe(future_df, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if show_processed_data:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("Processed Data")
            st.dataframe(analyzed_df, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if show_raw_data:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("Raw Data")
            st.dataframe(raw_df, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

    except ValueError as error:
        st.error(str(error))
    except Exception as error:
        st.error(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    main()
