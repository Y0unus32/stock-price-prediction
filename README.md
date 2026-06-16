# Stock Price Prediction

This project predicts the next trading day's stock closing price using historical market data. It downloads data from Yahoo Finance, builds technical indicators, trains machine learning models, evaluates them with a time-based split, and optionally runs a Streamlit web app for interactive predictions.

## Problem Statement

Stock price forecasting is a challenging research problem because prices are influenced by company performance, investor sentiment, economic indicators, global news, and market volatility. A useful prediction system can support traders, investors, and analysts by estimating the likely future direction of a stock.

## Dataset

The project uses historical stock data from Yahoo Finance through the `yfinance` Python package. This satisfies the dataset requirement using an open financial data platform.

Default stock: `AAPL`

You can change the ticker to any Yahoo Finance symbol, such as:

- `MSFT` - Microsoft
- `GOOGL` - Alphabet
- `TSLA` - Tesla
- `RELIANCE.NS` - Reliance Industries on NSE
- `TCS.NS` - Tata Consultancy Services on NSE

## Features Used

The model uses historical price and volume-based features:

- Open, High, Low, Close, Adjusted Close, Volume
- Daily return
- Moving averages
- Rolling volatility
- Price momentum
- Lagged closing prices

Target variable: next trading day's adjusted closing price.

## Models

The training script compares:

- Linear Regression
- Random Forest Regressor
- Gradient Boosting Regressor

The best model is selected using RMSE on the test set.

## Project Structure

```text
.
+-- README.md
+-- requirements.txt
+-- src
|   +-- app.py
|   +-- stock_prediction.py
|   +-- __init__.py
+-- outputs
    +-- .gitkeep
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
python src/stock_prediction.py --ticker AAPL --start 2015-01-01 --end 2026-01-01
```

Example for an Indian stock:

```bash
python src/stock_prediction.py --ticker RELIANCE.NS --start 2015-01-01 --end 2026-01-01
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

## Important Note

This project is for educational and research purposes only. Stock prices are noisy and affected by many unpredictable events, so predictions should not be treated as financial advice.
