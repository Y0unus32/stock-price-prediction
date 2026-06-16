# Stock Price Prediction

This project predicts the next trading day's stock closing price using historical market data. It downloads data from Yahoo Finance, builds technical indicators, trains machine learning models, evaluates them with a time-based split, and runs a modern Streamlit web app with an interactive dashboard.

## Problem Statement

Stock price forecasting is a challenging research problem because prices are influenced by company performance, investor sentiment, economic indicators, global news, and market volatility. A useful prediction system can support traders, investors, and analysts by estimating the likely future direction of a stock.

## Features

### 🏠 Home Dashboard
- Quick predictions for 8 popular stocks (AAPL, GOOGL, MSFT, AMZN, TSLA, META, NVDA, AMD)
- Live comparison table showing all stocks' predictions, models, and performance metrics

### 📊 Single Stock Prediction
- Detailed analysis for any stock ticker
- Multiple visualizations including:
  - Actual vs Predicted prices chart
  - Prediction error analysis
  - Model performance metrics
  - Detailed prediction data table
- Customizable date range selection

### 🔄 Batch Predictions
- Analyze multiple stocks simultaneously
- Progress tracking for batch processing
- Comprehensive summary table with all metrics

### ⚡ Performance Optimizations
- Data caching (1-hour TTL) to reduce API calls
- Session-based result caching to avoid redundant processing
- Efficient data loading and processing

### 🎨 Modern UI/UX
- Clean, intuitive navigation with sidebar
- Emoji-enhanced interface for visual appeal
- Responsive layouts with tabs and columns
- Improved error handling and user feedback

## Dataset

The project uses historical stock data from Yahoo Finance through the `yfinance` Python package. This satisfies the dataset requirement using an open financial data platform.

Default stocks: `AAPL`, `GOOGL`, `MSFT`, `AMZN`, `TSLA`, `META`, `NVDA`, `AMD`

You can analyze any Yahoo Finance symbol, such as:

- `MSFT` - Microsoft
- `TSLA` - Tesla
- `RELIANCE.NS` - Reliance Industries on NSE
- `TCS.NS` - Tata Consultancy Services on NSE

## Features Used

The model uses historical price and volume-based features:

- Open, High, Low, Close, Adjusted Close, Volume
- Daily return
- Moving averages (5, 10, 20 days)
- Rolling volatility
- Price momentum
- Volume change
- Lagged closing prices (1-5 days)

Target variable: next trading day's adjusted closing price.

## Models

The training script compares:

- Linear Regression
- Random Forest Regressor (300 estimators)
- Gradient Boosting Regressor

The best model is selected using RMSE on the test set.

## Project Structure

```text
.
+-- README.md
+-- requirements.txt
+-- src
|   +-- app.py                 # Streamlit web app
|   +-- stock_prediction.py    # ML pipeline
|   +-- __init__.py
+-- outputs
    +-- best_model.joblib     # Trained model
    +-- metrics.csv           # Model metrics
    +-- predictions.csv       # Predictions
    +-- prediction_plot.png   # Visualization
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Train From Command Line

```bash
python src/stock_prediction.py --ticker AAPL --start 2015-01-01 --end 2026-06-16
```

Example for an Indian stock:

```bash
python src/stock_prediction.py --ticker RELIANCE.NS --start 2015-01-01 --end 2026-06-16
```

The script saves:

- Trained model: `outputs/best_model.joblib`
- Metrics: `outputs/metrics.csv`
- Predictions: `outputs/predictions.csv`
- Plot: `outputs/prediction_plot.png`

## Run Web App

```bash
streamlit run src/app.py
```

The app will open in your browser with three pages:

1. **Home** - Dashboard with popular stocks
2. **Predict Single Stock** - Detailed analysis for any ticker
3. **Batch Predict** - Analyze multiple stocks at once

## Recent Improvements

✅ Added home page with multiple stocks  
✅ Implemented data caching for better performance  
✅ Enhanced visualizations with error analysis  
✅ Improved UI with tabs and better layouts  
✅ Added batch prediction functionality  
✅ Better error handling and user feedback  

## Important Note

This project is for educational and research purposes only. Stock prices are noisy and affected by many unpredictable events, so predictions should not be treated as financial advice.
