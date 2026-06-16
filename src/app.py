from __future__ import annotations

from datetime import date

import streamlit as st

from stock_prediction import train_and_predict


st.set_page_config(page_title="Stock Price Prediction", layout="wide")

st.title("Stock Price Prediction")

with st.sidebar:
    ticker = st.text_input("Ticker", value="AAPL").strip().upper()
    start_date = st.date_input("Start date", value=date(2015, 1, 1))
    end_date = st.date_input("End date", value=date.today())
    run_button = st.button("Train and Predict", type="primary")

if run_button:
    if not ticker:
        st.error("Enter a valid ticker symbol.")
    elif start_date >= end_date:
        st.error("Start date must be earlier than end date.")
    else:
        with st.spinner("Downloading data, training models, and preparing predictions..."):
            result = train_and_predict(
                ticker=ticker,
                start=start_date.isoformat(),
                end=end_date.isoformat(),
            )

        st.subheader(f"Prediction for {result.ticker}")
        st.metric("Predicted next trading day close", f"{result.next_day_prediction:,.2f}")
        st.caption(f"Best model selected by lowest RMSE: {result.best_model_name}")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("Model Metrics")
            st.dataframe(result.metrics, use_container_width=True, hide_index=True)

        with col2:
            st.subheader("Actual vs Predicted")
            chart_data = result.predictions.set_index("Date")[["Actual", "Predicted"]]
            st.line_chart(chart_data)

        st.subheader("Recent Predictions")
        st.dataframe(result.predictions.tail(20), use_container_width=True, hide_index=True)
else:
    st.info("Choose a ticker and date range, then click Train and Predict.")
