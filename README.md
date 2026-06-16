# Stock Price Prediction 📈

Predict next trading day's stock closing price using Machine Learning models powered by Streamlit.

**Live App:** https://stock-price-prediction-y0unus32.streamlit.app/

This project downloads historical stock data from Yahoo Finance, builds technical indicators, trains multiple ML models, and provides an interactive web interface for predictions.

## Features ✨

### App Features
- 🎯 **Real-time Predictions** - Get next day's stock price prediction instantly
- 📊 **Model Comparison** - Compare performance of Linear Regression, Random Forest, and Gradient Boosting
- 📉 **Technical Indicators** - Visualize moving averages, volatility, and momentum
- 💾 **Export Data** - Download predictions and metrics as CSV files
- ⚡ **Smart Caching** - Results cached for 1 hour (results load instantly for same ticker/date range)
- 🏢 **Company Info** - Display sector, industry, and currency information
- 🌍 **Global Support** - Works with any Yahoo Finance ticker (US stocks, Indian NSE/BSE, etc.)

### ML Features
- Historical price and volume analysis
- Moving averages (5, 10, 20 day)
- Rolling volatility calculation
- Price momentum indicators
- Lagged price features
- Time-series train/test split
- Multiple model ensemble

## Problem Statement

Stock price forecasting is challenging due to market complexity. This system helps traders, investors, and analysts by providing ML-based price predictions using historical data patterns.

## Dataset

Historical stock data from **Yahoo Finance** via `yfinance` package.

Supported tickers:
- **US Stocks:** AAPL, MSFT, GOOGL, TSLA, AMZN, META, NVIDIA, etc.
- **Indian Stocks:** RELIANCE.NS, TCS.NS, INFY.NS, etc.
- **International:** Any Yahoo Finance symbol

## Models

The app compares three ML algorithms:

| Model | Best For | Speed |
|-------|----------|-------|
| **Linear Regression** | Baseline, trend detection | ⚡ Fastest |
| **Random Forest** | Non-linear patterns | ⚡ Fast |
| **Gradient Boosting** | Complex relationships | 🐢 Slower but powerful |

Best model selected by **lowest RMSE** on test set.

## Project Structure

```
.
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── src/
│   ├── app.py               # Streamlit web app
│   ├── stock_prediction.py  # ML training pipeline
│   └── __init__.py
└── outputs/
    ├── best_model.joblib    # Trained model (cached)
    ├── metrics.csv          # Model performance metrics
    ├── predictions.csv      # Historical predictions
    └── prediction_plot.png  # Visualization
```

## Installation

### Prerequisites
- Python 3.9+
- pip or conda

### Setup

1. **Clone repository**
   ```bash
   git clone https://github.com/Y0unus32/stock-price-prediction.git
   cd stock-price-prediction
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate    # Windows
   source .venv/bin/activate # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Web App (Recommended)

```bash
streamlit run src/app.py
```

Then open http://localhost:8501 in your browser.

**Options:**
- Enter stock ticker (e.g., AAPL, TSLA, RELIANCE.NS)
- Select date range (minimum 6 months recommended)
- Toggle "Show Technical Indicators" to see moving averages and volatility
- Toggle "Compare All Models" to see performance comparison
- Download predictions as CSV

### Command Line

```bash
python src/stock_prediction.py --ticker AAPL --start 2015-01-01 --end 2024-12-31
```

**Options:**
- `--ticker`: Stock symbol (default: AAPL)
- `--start`: Start date (default: 2015-01-01)
- `--end`: End date (default: today)

**Output files saved to `outputs/`:**
- `best_model.joblib` - Trained model
- `metrics.csv` - Model performance
- `predictions.csv` - Price predictions
- `prediction_plot.png` - Chart

### Example: Indian Stock

```bash
streamlit run src/app.py
# Then enter: RELIANCE.NS, TCS.NS, etc.
```

## Performance

- **Training time**: 10-30 seconds (cached after first run)
- **Prediction speed**: < 1 second
- **Cache duration**: 1 hour (results reused automatically)
- **Model accuracy**: R² typically 0.85-0.95 on test set

## Technical Details

### Features Used
- **Price Data**: Open, High, Low, Close, Volume, Adjusted Close
- **Technical Indicators**: 
  - Daily returns
  - Moving averages (5, 10, 20 day)
  - Volatility (10-day rolling std)
  - Momentum (10-day price change)
  - Volume changes
- **Lagged Features**: Previous 5 days closing prices

### Evaluation Metrics
- **MAE** (Mean Absolute Error): Average prediction error in dollars
- **RMSE** (Root Mean Squared Error): Penalizes larger errors
- **R²**: Proportion of variance explained (0-1, higher is better)

## Dependencies

See [requirements.txt](requirements.txt):
- pandas >= 2.0.0
- numpy >= 1.24.0
- scikit-learn >= 1.3.0
- yfinance >= 0.2.40
- matplotlib >= 3.7.0
- joblib >= 1.3.0
- streamlit >= 1.30.0

## Limitations & Disclaimers ⚠️

1. **Educational Purpose**: This project is for learning and research only
2. **Not Financial Advice**: Predictions should NOT be used for real trading decisions
3. **Market Unpredictability**: Stock prices depend on countless unpredictable factors:
   - Geopolitical events
   - Company news and earnings
   - Market sentiment
   - Economic indicators
   - Black swan events
4. **Historical Patterns**: Model uses historical data; past performance ≠ future results
5. **Data Quality**: Yahoo Finance data may have gaps or errors

**Always consult a financial advisor before making investment decisions.**

## Future Enhancements 🚀

- [ ] LSTM/RNN models for sequence prediction
- [ ] Ensemble methods combining all models
- [ ] Confidence intervals for predictions
- [ ] Multi-step ahead forecasting (1-week, 1-month)
- [ ] Real-time alerts for price movements
- [ ] Portfolio analysis for multiple stocks
- [ ] Advanced technical indicators (RSI, MACD, Bollinger Bands)
- [ ] XGBoost and LightGBM models

## Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## License

MIT License - See LICENSE file for details

## Author

Created by [Y0unus32](https://github.com/Y0unus32)
