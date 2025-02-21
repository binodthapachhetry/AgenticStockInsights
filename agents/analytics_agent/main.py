from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok", "service": "analytics-agent"}

@app.get("/stock_sentiment_correlations")
def stock_sentiment_correlations(ticker: str):
    """
    Example endpoint to fetch historical sentiment and price data,
    then compute correlation.
    """
    # Pseudocode: fetch sentiment from BigQuery or Elasticsearch
    # fetch prices from yfinance or BigQuery

    # mock data
    data = {
        "date": pd.date_range("2025-01-01", periods=5).strftime("%Y-%m-%d").tolist(),
        "price": [100, 102, 105, 103, 110],
        "sentiment": [0.1, 0.2, -0.1, 0.3, 0.4]
    }
    df = pd.DataFrame(data)
    corr = df["price"].corr(df["sentiment"])
    return {
        "ticker": ticker,
        "corr": corr,
        "data_points": df.to_dict(orient="records")
    }