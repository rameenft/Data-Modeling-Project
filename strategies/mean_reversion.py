"""
strategies/mean_reversion.py
-----------------------------
Single-stock mean reversion strategy.

Signal: compute the z-score of the current price vs its rolling mean over
        `lookback` days. If z-score < -1 (price is unusually low), buy (1.0).
        Otherwise hold cash (0.0).
"""

import pandas as pd
import numpy as np
from strategies.base import BaseStrategy


class MeanReversionStrategy(BaseStrategy):
    def __init__(self, lookback: int = 20, ticker: str = "AAPL", z_threshold: float = -1.0):
        super().__init__(name=f"MeanReversion(lookback={lookback}, {ticker})")
        self.lookback = lookback
        self.ticker = ticker
        self.z_threshold = z_threshold

    def generate_weights(self, prices: pd.DataFrame, current_date: pd.Timestamp) -> pd.Series:
        history = self._no_lookahead(prices, current_date)[self.ticker].dropna()

        if len(history) < self.lookback:
            return pd.Series({self.ticker: 0.0})

        window = history.iloc[-self.lookback:]
        mean = window.mean()
        std = window.std()

        if std == 0:
            return pd.Series({self.ticker: 0.0})

        z_score = (history.iloc[-1] - mean) / std
        weight = 1.0 if z_score < self.z_threshold else 0.0
        return pd.Series({self.ticker: weight})
