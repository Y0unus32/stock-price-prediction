from __future__ import annotations

from datetime import date
import io

import streamlit as st
import pandas as pd

from stock_prediction import train_and_predict, get_stock_info, calculate_technical_indicators


st.set_page_config(page_title="Stock Price Prediction", layout="wide")


# Cache the prediction function to avoid retraining on reruns
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_prediction(ticker: str, start: str, end: str):
    return train_and_predict(ticker=ticker, start=start, end=end)


st.title("📈 Stock Price Prediction")
st.markdown("Predict next trading day's stock price using Machine Learning models")

with st.sidebar:
    st.header("⚙️ Configuration")
    ticker = st.text_input("Stock Ticker", value="AAPL").strip().upper()
    start_date = st.date_input("Start date", value=date(2015, 1, 1))
    end_date = st.date_input("End date", value=date.today())
    
    st.divider()
    st.subheader("Options")
    show_technical = st.checkbox("Show Technical Indicators", value=True)
    show_all_models = st.checkbox("Compare All Models", value=False)
    
    run_button = st.button("🚀 Train and Predict", type="primary", use_container_width=True)

if run_button:
    if not ticker:
        st.error("❌ Enter a valid ticker symbol.")
    elif start_date >= end_date:
        st.error("❌ Start date must be earlier than end date.")
    else:
        try:
            with st.spinner("⏳ Downloading data, training models, and preparing predictions..."):
                result = get_prediction(
                    ticker=ticker,
                    start=start_date.isoformat(),
                    end=end_date.isoformat(),
                )
            
            # Stock Info
            stock_info = get_stock_info(ticker)
            if stock_info:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Company", stock_info.get("Company", "N/A")[:15])
                with col2:
                    st.metric("Sector", stock_info.get("Sector", "N/A")[:15])
                with col3:
                    st.metric("Industry", stock_info.get("Industry", "N/A")[:15])
                with col4:
                    st.metric("Currency", stock_info.get("Currency", "N/A"))
                st.divider()
            
            # Prediction Summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🎯 Predicted Price", f"${result.next_day_prediction:,.2f}")
            with col2:
                st.metric("📊 Best Model", result.best_model_name)
            with col3:
                best_rmse = result.metrics.iloc[0]["RMSE"]
                st.metric("✅ Model RMSE", f"${best_rmse:,.2f}")
            
            st.divider()
            
            # Model Metrics
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("📊 Best Model Metrics")
                best_metrics = result.metrics.iloc[0][["Model", "MAE", "RMSE", "R2"]].to_frame()
                st.dataframe(best_metrics, use_container_width=True)
            
            with col2:
                st.subheader("📈 Actual vs Predicted")
                chart_data = result.predictions.set_index("Date")[["Actual", "Predicted"]]
                st.line_chart(chart_data, use_container_width=True)
            
            # All Models Comparison
            if show_all_models:
                st.subheader("🏆 Model Comparison")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.dataframe(result.metrics, use_container_width=True, hide_index=True)
                
                with col2:
                    # Model Performance Chart
                    chart_df = result.metrics[["Model", "RMSE"]].set_index("Model")
                    st.bar_chart(chart_df, use_container_width=True)
            
            # Technical Indicators
            if show_technical:
                st.subheader("📉 Technical Indicators")
                tech_data = calculate_technical_indicators(result.predictions)
                if tech_data is not None:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Moving Averages & Momentum**")
                        st.line_chart(tech_data[["Actual", "MA_5", "MA_10", "MA_20"]], use_container_width=True)
                    
                    with col2:
                        st.write("**Volatility (20-day)**")
                        st.area_chart(tech_data[["Volatility"]], use_container_width=True)
            
            # Recent Predictions Table
            st.subheader("📋 Recent Predictions")
            recent = result.predictions.tail(20).copy()
            recent["Date"] = pd.to_datetime(recent["Date"]).dt.strftime("%Y-%m-%d")
            recent["Actual"] = recent["Actual"].apply(lambda x: f"${x:,.2f}")
            recent["Predicted"] = recent["Predicted"].apply(lambda x: f"${x:,.2f}")
            st.dataframe(recent, use_container_width=True, hide_index=True)
            
            # Export Option
            st.divider()
            st.subheader("💾 Export")
            col1, col2 = st.columns(2)
            
            with col1:
                csv = result.predictions.to_csv(index=False)
                st.download_button(
                    label="📥 Download Predictions (CSV)",
                    data=csv,
                    file_name=f"{ticker}_predictions.csv",
                    mime="text/csv"
                )
            
            with col2:
                metrics_csv = result.metrics.to_csv(index=False)
                st.download_button(
                    label="📥 Download Model Metrics (CSV)",
                    data=metrics_csv,
                    file_name=f"{ticker}_metrics.csv",
                    mime="text/csv"
                )

        except ValueError as e:
            st.error(f"❌ Error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            st.info("💡 Try a different ticker or date range")
else:
    st.info("👈 **How to use:**\n1. Enter a stock ticker (e.g., AAPL, GOOGL, TSLA)\n2. Select your date range\n3. Click 'Train and Predict'\n\n**Example tickers:** AAPL, MSFT, GOOGL, TSLA, AMZN, META, NVIDIA")
