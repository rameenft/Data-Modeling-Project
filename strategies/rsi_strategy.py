"""
strategies/rsi_strategy.py
---------------------------
Single-stock RSI (Relative Strength Index) contrarian strategy.

Signal: RSI < oversold threshold → buy (1.0).
        RSI > overbought threshold → sell (0.0).
        Otherwise → hold previous position (simplified to: buy if oversold, else cash).
"""

import pandas as pd
import numpy as np
from strategies.base import BaseStrategy


def _compute_rsi(prices: pd.Series, period: int = 14) -> float:
    delta = prices.diff().dropna()
    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)
    avg_gain = gains.ewm(com=period - 1, adjust=False).mean().iloc[-1]
    avg_loss = losses.ewm(com=period - 1, adjust=False).mean().iloc[-1]
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


class RSIStrategy(BaseStrategy):
    def __init__(self, period: int = 14, oversold: float = 30.0, overbought: float = 70.0, ticker: str = "AAPL"):
        super().__init__(name=f"RSI(period={period}, {ticker})")
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
        self.ticker = ticker
        self._in_position = False

    def generate_weights(self, prices: pd.DataFrame, current_date: pd.Timestamp) -> pd.Series:
        history = self._no_lookahead(prices, current_date)[self.ticker].dropna()

        if len(history) < self.period + 1:
            return pd.Series({self.ticker: 0.0})

        rsi = _compute_rsi(history, self.period)

        if rsi < self.oversold:
            self._in_position = True
        elif rsi > self.overbought:
            self._in_position = False

        weight = 1.0 if self._in_position else 0.0
        return pd.Series({self.ticker: weight})
