"""
strategies/macd.py
------------------
Single-stock MACD (Moving Average Convergence Divergence) strategy.

Signal: MACD line = EMA(12) - EMA(26). Signal line = EMA(9) of MACD.
        Buy (1.0) when MACD crosses above signal line; sell (0.0) when below.
"""

import pandas as pd
from strategies.base import BaseStrategy


class MACDStrategy(BaseStrategy):
    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9, ticker: str = "AAPL"):
        super().__init__(name=f"MACD({fast},{slow},{signal}, {ticker})")
        self.fast = fast
        self.slow = slow
        self.signal = signal
        self.ticker = ticker

    def generate_weights(self, prices: pd.DataFrame, current_date: pd.Timestamp) -> pd.Series:
        history = self._no_lookahead(prices, current_date)[self.ticker].dropna()
        min_required = self.slow + self.signal
        if len(history) < min_required:
            return pd.Series({self.ticker: 0.0})

        ema_fast = history.ewm(span=self.fast, adjust=False).mean()
        ema_slow = history.ewm(span=self.slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=self.signal, adjust=False).mean()

        weight = 1.0 if macd_line.iloc[-1] > signal_line.iloc[-1] else 0.0
        return pd.Series({self.ticker: weight})
