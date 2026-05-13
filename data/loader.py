"""
data/loader.py
--------------
Loads and preprocesses the Nasdaq-100 daily CSV into a clean price matrix.
"""

import pandas as pd
from pathlib import Path


def load_prices(csv_path: str | Path) -> pd.DataFrame:
    """
    Load the Nasdaq-100 daily CSV and return a DataFrame of closing prices.

    Returns
    -------
    pd.DataFrame
        Index  : datetime dates (trading days)
        Columns: ticker symbols
        Values : adjusted closing prices
    """
    df = pd.read_csv(csv_path, parse_dates=["date"])
    df = df[["ticker", "date", "close"]].copy()
    df = df.dropna(subset=["close"])

    # Pivot to wide format: rows = dates, columns = tickers
    prices = df.pivot(index="date", columns="ticker", values="close")
    prices = prices.sort_index()

    return prices


def get_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Compute daily log returns from a price matrix.

    Returns
    -------
    pd.DataFrame
        Same shape as prices, with NaN on the first row.
    """
    return prices.pct_change()
