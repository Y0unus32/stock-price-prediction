from __future__ import annotations

from datetime import date, timedelta
import streamlit as st
import pandas as pd
from stock_prediction import train_and_predict

st.set_page_config(
    page_title="Stock Price Prediction",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "predictions_cache" not in st.session_state:
    st.session_state.predictions_cache = {}

st.title("📈 Stock Price Prediction")

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Home", "Predict Single Stock", "Batch Predict"])

if page == "Home":
    st.markdown("---")
    st.subheader("Quick Stock Predictions")

    popular_stocks = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META", "NVDA", "AMD"]

    st.info("💡 Showing predictions for popular stocks. Click on any stock to see detailed analysis.")

    # Create columns for stock cards
    cols = st.columns(4)
    results = {}

    for idx, ticker in enumerate(popular_stocks):
        col = cols[idx % 4]

        with col:
            with st.spinner(f"Loading {ticker}..."):
                try:
                    if ticker not in st.session_state.predictions_cache:
                        result = train_and_predict(
                            ticker=ticker,
                            start="2020-01-01",
                            end=date.today().isoformat(),
                        )
                        st.session_state.predictions_cache[ticker] = result
                    else:
                        result = st.session_state.predictions_cache[ticker]

                    results[ticker] = result

                    col.metric(
                        f"{ticker}",
                        f"${result.next_day_prediction:,.2f}",
                        f"Best: {result.best_model_name}"
                    )

                    col.caption(f"RMSE: {result.metrics.iloc[0]['RMSE']:.2f}")

                except Exception as e:
                    col.error(f"Error loading {ticker}: {str(e)[:50]}")

    st.markdown("---")
    st.subheader("Stock Performance Overview")

    # Create comparison table
    if results:
        comparison_data = []
        for ticker, result in results.items():
            comparison_data.append({
                "Ticker": ticker,
                "Next Day Prediction": f"${result.next_day_prediction:,.2f}",
                "Best Model": result.best_model_name,
                "RMSE": f"{result.metrics.iloc[0]['RMSE']:.2f}",
                "R² Score": f"{result.metrics.iloc[0]['R2']:.4f}",
            })

        st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)

elif page == "Predict Single Stock":
    st.subheader("Single Stock Prediction")

    with st.sidebar:
        st.markdown("### Configuration")
        ticker = st.text_input("Stock Ticker", value="AAPL", placeholder="e.g., AAPL, GOOGL").strip().upper()
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start date", value=date(2020, 1, 1))
        with col2:
            end_date = st.date_input("End date", value=date.today())
        run_button = st.button("🚀 Train and Predict", type="primary", use_container_width=True)

    if run_button:
        if not ticker:
            st.error("⚠️ Enter a valid ticker symbol.")
        elif start_date >= end_date:
            st.error("⚠️ Start date must be earlier than end date.")
        else:
            try:
                with st.spinner("Downloading data, training models, and preparing predictions..."):
                    result = train_and_predict(
                        ticker=ticker,
                        start=start_date.isoformat(),
                        end=end_date.isoformat(),
                    )

                # Key metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Predicted Next Close", f"${result.next_day_prediction:,.2f}")
                with col2:
                    st.metric("Best Model", result.best_model_name)
                with col3:
                    st.metric("Best RMSE", f"{result.metrics.iloc[0]['RMSE']:.2f}")

                st.markdown("---")

                # Charts and metrics
                tab1, tab2, tab3 = st.tabs(["📊 Chart", "📈 Metrics", "📋 Data"])

                with tab1:
                    st.subheader("Actual vs Predicted Prices")
                    chart_data = result.predictions.set_index("Date")[["Actual", "Predicted"]]
                    st.line_chart(chart_data, use_container_width=True)

                    st.subheader("Prediction Error Over Time")
                    result.predictions["Error"] = abs(result.predictions["Actual"] - result.predictions["Predicted"])
                    error_data = result.predictions.set_index("Date")[["Error"]]
                    st.area_chart(error_data, use_container_width=True)

                with tab2:
                    st.subheader("Model Metrics")
                    st.dataframe(result.metrics, use_container_width=True, hide_index=True)

                with tab3:
                    st.subheader("Recent Predictions (Last 20 Days)")
                    st.dataframe(result.predictions.tail(20), use_container_width=True, hide_index=True)

            except ValueError as e:
                st.error(f"⚠️ {str(e)}")
            except Exception as e:
                st.error(f"⚠️ An error occurred: {str(e)}")
    else:
        st.info("👈 Enter a ticker and date range in the sidebar, then click 'Train and Predict'")

elif page == "Batch Predict":
    st.subheader("Batch Stock Predictions")
    st.markdown("Predict multiple stocks at once.")

    with st.sidebar:
        st.markdown("### Batch Configuration")
        tickers_input = st.text_area(
            "Enter tickers (one per line)",
            value="AAPL\nGOOGL\nMSFT",
            height=150,
        )
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start date", value=date(2020, 1, 1), key="batch_start")
        with col2:
            end_date = st.date_input("End date", value=date.today(), key="batch_end")
        run_batch = st.button("🚀 Predict All", type="primary", use_container_width=True)

    if run_batch:
        tickers = [t.strip().upper() for t in tickers_input.split("\n") if t.strip()]

        if not tickers:
            st.error("⚠️ Enter at least one ticker.")
        elif start_date >= end_date:
            st.error("⚠️ Start date must be earlier than end date.")
        else:
            progress_bar = st.progress(0)
            results_list = []

            for i, ticker in enumerate(tickers):
                try:
                    with st.spinner(f"Processing {ticker} ({i+1}/{len(tickers)})..."):
                        result = train_and_predict(
                            ticker=ticker,
                            start=start_date.isoformat(),
                            end=end_date.isoformat(),
                        )
                        results_list.append(result)
                except Exception as e:
                    st.warning(f"Failed to process {ticker}: {str(e)[:50]}")

                progress_bar.progress((i + 1) / len(tickers))

            if results_list:
                st.success(f"✅ Successfully processed {len(results_list)} stocks")

                # Summary table
                summary_data = []
                for result in results_list:
                    summary_data.append({
                        "Ticker": result.ticker,
                        "Next Day Prediction": f"${result.next_day_prediction:,.2f}",
                        "Best Model": result.best_model_name,
                        "RMSE": f"{result.metrics.iloc[0]['RMSE']:.2f}",
                        "R² Score": f"{result.metrics.iloc[0]['R2']:.4f}",
                    })

                st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)
    else:
        st.info("👈 Enter tickers in the sidebar and click 'Predict All'")
