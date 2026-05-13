"""
portfolio/constructor.py
------------------------
Portfolio construction helpers: converts a list of selected stocks and optional
signals into a normalized weight vector across all tickers.
"""

import pandas as pd
import numpy as np


def uniform_weights(selected: list[str], all_tickers: list[str]) -> pd.Series:
    """Equal weight across selected stocks; zero for all others."""
    weights = pd.Series(0.0, index=all_tickers)
    if selected:
        weights[selected] = 1.0 / len(selected)
    return weights


def risk_adjusted_weights(
    selected: list[str],
    volatilities: pd.Series,
    all_tickers: list[str],
) -> pd.Series:
    """
    Weights inversely proportional to rolling volatility among selected stocks.
    Stocks with lower vol get higher allocation.
    """
    weights = pd.Series(0.0, index=all_tickers)
    if not selected:
        return weights

    inv_vol = 1.0 / volatilities[selected].replace(0, np.nan).dropna()
    if inv_vol.empty:
        return uniform_weights(selected, all_tickers)

    normalized = inv_vol / inv_vol.sum()
    weights[normalized.index] = normalized
    return weights


def rolling_volatility(prices: pd.DataFrame, window: int) -> pd.Series:
    """Annualized rolling volatility for each stock using the last `window` days."""
    returns = prices.pct_change().iloc[-window:]
    vol = returns.std() * np.sqrt(252)
    return vol
