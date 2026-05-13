"""
strategies/bollinger_band.py
-----------------------------
Single-stock Bollinger Band mean-reversion strategy.

Signal: Buy (1.0) when price drops below the lower band (mean - 2*std).
        Sell (0.0) when price rises above the upper band (mean + 2*std).
        Hold previous position otherwise (implemented as: buy if below lower,
        cash if above upper, no change otherwise — simplified to binary).
"""

import pandas as pd
from strategies.base import BaseStrategy


class BollingerBandStrategy(BaseStrategy):
    def __init__(self, window: int = 20, num_std: float = 2.0, ticker: str = "AAPL"):
        super().__init__(name=f"BollingerBand(window={window}, {ticker})")
        self.window = window
        self.num_std = num_std
        self.ticker = ticker
        self._in_position = False

    def generate_weights(self, prices: pd.DataFrame, current_date: pd.Timestamp) -> pd.Series:
        history = self._no_lookahead(prices, current_date)[self.ticker].dropna()

        if len(history) < self.window:
            return pd.Series({self.ticker: 0.0})

        window_data = history.iloc[-self.window:]
        mean = window_data.mean()
        std = window_data.std()
        current_price = history.iloc[-1]
        lower = mean - self.num_std * std
        upper = mean + self.num_std * std

        if current_price < lower:
            self._in_position = True
        elif current_price > upper:
            self._in_position = False

        weight = 1.0 if self._in_position else 0.0
        return pd.Series({self.ticker: weight})
