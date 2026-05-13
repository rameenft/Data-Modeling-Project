"""
strategies/risk_adjusted_momentum.py
--------------------------------------
New Strategy 1 (portfolio-level): Risk-Adjusted Momentum with RSI Filter.

Steps:
  1. Compute 30-day trailing return for all stocks (momentum signal).
  2. Filter out overbought stocks (RSI > 70) to avoid chasing extended moves.
  3. Select the top K stocks by momentum from the remaining pool.
  4. Allocate inversely proportional to 20-day rolling volatility (lower vol → higher weight).

This combines momentum with a risk-quality filter, aiming for a better
risk-adjusted return than raw top-K momentum.
"""

import pandas as pd
import numpy as np
from strategies.base import BaseStrategy
from portfolio.constructor import risk_adjusted_weights, rolling_volatility


def _rsi(series: pd.Series, period: int = 14) -> float:
    delta = series.diff().dropna()
    gains = delta.clip(lower=0).ewm(com=period - 1, adjust=False).mean()
    losses = (-delta.clip(upper=0)).ewm(com=period - 1, adjust=False).mean()
    last_loss = losses.iloc[-1]
    if last_loss == 0:
        return 100.0
    return 100 - 100 / (1 + gains.iloc[-1] / last_loss)


class RiskAdjustedMomentumStrategy(BaseStrategy):
    def __init__(self, lookback: int = 30, top_k: int = 15, rsi_period: int = 14,
                 rsi_overbought: float = 70.0, vol_window: int = 20):
        super().__init__(name=f"RiskAdj_Momentum(K={top_k}, RSI_filter)")
        self.lookback = lookback
        self.top_k = top_k
        self.rsi_period = rsi_period
        self.rsi_overbought = rsi_overbought
        self.vol_window = vol_window

    def generate_weights(self, prices: pd.DataFrame, current_date: pd.Timestamp) -> pd.Series:
        history = self._no_lookahead(prices, current_date)
        all_tickers = prices.columns.tolist()
        min_required = max(self.lookback + 1, self.rsi_period + 1, self.vol_window)

        if len(history) < min_required:
            return pd.Series(0.0, index=all_tickers)

        # Step 1: momentum signal
        past_prices = history.iloc[-(self.lookback + 1)]
        current_prices = history.iloc[-1]
        trailing_returns = (current_prices - past_prices) / past_prices.replace(0, np.nan)

        # Step 2: RSI filter — exclude overbought
        not_overbought = []
        for ticker in all_tickers:
            series = history[ticker].dropna()
            if len(series) < self.rsi_period + 1:
                continue
            if _rsi(series, self.rsi_period) <= self.rsi_overbought:
                not_overbought.append(ticker)

        filtered_returns = trailing_returns[not_overbought].dropna()
        if filtered_returns.empty:
            return pd.Series(0.0, index=all_tickers)

        # Step 3: top K
        selected = filtered_returns.nlargest(self.top_k).index.tolist()

        # Step 4: risk-adjusted (inverse vol) weighting
        vols = rolling_volatility(history, self.vol_window)
        return risk_adjusted_weights(selected, vols, all_tickers)
