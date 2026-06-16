from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path

import joblib
import streamlit as st

os.environ.setdefault("MPLCONFIGDIR", str(Path("outputs") / "matplotlib-cache"))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


OUTPUT_DIR = Path("outputs")


@dataclass
class TrainResult:
    ticker: str
    best_model_name: str
    metrics: pd.DataFrame
    predictions: pd.DataFrame
    next_day_prediction: float


@st.cache_data(ttl=3600)
def download_stock_data(ticker: str, start: str, end: str | None = None) -> pd.DataFrame:
    data = yf.download(ticker, start=start, end=end, auto_adjust=False, progress=False)
    if data.empty:
        raise ValueError(f"No data found for ticker '{ticker}'. Check the symbol and date range.")

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.reset_index()
    data["Date"] = pd.to_datetime(data["Date"])
    return data


def build_features(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()

    price_col = "Adj Close" if "Adj Close" in df.columns else "Close"
    df = df.rename(columns={price_col: "Price"})

    df["Daily_Return"] = df["Price"].pct_change()
    df["MA_5"] = df["Price"].rolling(window=5).mean()
    df["MA_10"] = df["Price"].rolling(window=10).mean()
    df["MA_20"] = df["Price"].rolling(window=20).mean()
    df["Volatility_10"] = df["Daily_Return"].rolling(window=10).std()
    df["Momentum_10"] = df["Price"] - df["Price"].shift(10)
    df["Volume_Change"] = df["Volume"].pct_change()

    for lag in range(1, 6):
        df[f"Price_Lag_{lag}"] = df["Price"].shift(lag)

    df["Target_Next_Close"] = df["Price"].shift(-1)
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    return df


def split_time_series(
    df: pd.DataFrame, feature_columns: list[str], target_column: str, train_ratio: float = 0.8
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    split_index = int(len(df) * train_ratio)
    train_df = df.iloc[:split_index]
    test_df = df.iloc[split_index:]

    x_train = train_df[feature_columns]
    x_test = test_df[feature_columns]
    y_train = train_df[target_column]
    y_test = test_df[target_column]
    return x_train, x_test, y_train, y_test


def get_models() -> dict[str, object]:
    return {
        "Linear Regression": Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                ("model", LinearRegression()),
            ]
        ),
        "Random Forest": RandomForestRegressor(
            n_estimators=300,
            random_state=42,
            min_samples_leaf=2,
            n_jobs=-1,
        ),
        "Gradient Boosting": GradientBoostingRegressor(random_state=42),
    }


def evaluate_model(y_true: pd.Series, y_pred: np.ndarray) -> dict[str, float]:
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    return {
        "MAE": float(mean_absolute_error(y_true, y_pred)),
        "RMSE": rmse,
        "R2": float(r2_score(y_true, y_pred)),
    }


def plot_predictions(predictions: pd.DataFrame, output_path: Path) -> None:
    plt.figure(figsize=(12, 6))
    plt.plot(predictions["Date"], predictions["Actual"], label="Actual", linewidth=2)
    plt.plot(predictions["Date"], predictions["Predicted"], label="Predicted", linewidth=2)
    plt.title("Actual vs Predicted Stock Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def train_and_predict(ticker: str, start: str, end: str | None = None, output_dir: Path = OUTPUT_DIR) -> TrainResult:
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_data = download_stock_data(ticker=ticker, start=start, end=end)
    df = build_features(raw_data)

    feature_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Daily_Return",
        "MA_5",
        "MA_10",
        "MA_20",
        "Volatility_10",
        "Momentum_10",
        "Volume_Change",
        "Price_Lag_1",
        "Price_Lag_2",
        "Price_Lag_3",
        "Price_Lag_4",
        "Price_Lag_5",
    ]
    target_column = "Target_Next_Close"

    x_train, x_test, y_train, y_test = split_time_series(df, feature_columns, target_column)
    models = get_models()

    rows = []
    fitted_models = {}
    for name, model in models.items():
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        metrics = evaluate_model(y_test, y_pred)
        rows.append({"Model": name, **metrics})
        fitted_models[name] = model

    metrics_df = pd.DataFrame(rows).sort_values("RMSE").reset_index(drop=True)
    best_model_name = str(metrics_df.iloc[0]["Model"])
    best_model = fitted_models[best_model_name]

    test_predictions = best_model.predict(x_test)
    predictions = pd.DataFrame(
        {
            "Date": df.iloc[len(x_train) :]["Date"].values,
            "Actual": y_test.values,
            "Predicted": test_predictions,
        }
    )

    latest_features = df[feature_columns].iloc[[-1]]
    next_day_prediction = float(best_model.predict(latest_features)[0])

    joblib.dump(best_model, output_dir / "best_model.joblib")
    metrics_df.to_csv(output_dir / "metrics.csv", index=False)
    predictions.to_csv(output_dir / "predictions.csv", index=False)
    plot_predictions(predictions, output_dir / "prediction_plot.png")

    return TrainResult(
        ticker=ticker,
        best_model_name=best_model_name,
        metrics=metrics_df,
        predictions=predictions,
        next_day_prediction=next_day_prediction,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train stock price prediction models.")
    parser.add_argument("--ticker", default="AAPL", help="Yahoo Finance ticker symbol.")
    parser.add_argument("--start", default="2015-01-01", help="Start date in YYYY-MM-DD format.")
    parser.add_argument("--end", default=None, help="End date in YYYY-MM-DD format.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = train_and_predict(ticker=args.ticker, start=args.start, end=args.end)

    print(f"Ticker: {result.ticker}")
    print(f"Best model: {result.best_model_name}")
    print("\nModel metrics:")
    print(result.metrics.to_string(index=False))
    print(f"\nPredicted next trading day close: {result.next_day_prediction:.2f}")
    print("\nSaved outputs in the outputs directory.")


if __name__ == "__main__":
    main()
