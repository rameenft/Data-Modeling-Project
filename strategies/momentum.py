"""
strategies/momentum.py
----------------------
Single-stock momentum strategy.

Signal: if the trailing return over `lookback` days is positive, hold 100%
        in the target stock; otherwise hold cash.
"""

import pandas as pd
from strategies.base import BaseStrategy


class MomentumStrategy(BaseStrategy):
    def __init__(self, lookback: int = 20, ticker: str = "AAPL"):
        super().__init__(name=f"Momentum(lookback={lookback}, {ticker})")
        self.lookback = lookback
        self.ticker = ticker

    def generate_weights(self, prices: pd.DataFrame, current_date: pd.Timestamp) -> pd.Series:
        history = self._no_lookahead(prices, current_date)

        if len(history) < self.lookback + 1:
            return pd.Series({self.ticker: 0.0})

        past_price = history[self.ticker].iloc[-(self.lookback + 1)]
        current_price = history[self.ticker].iloc[-1]

        if past_price <= 0:
            return pd.Series({self.ticker: 0.0})

        trailing_return = (current_price - past_price) / past_price
        weight = 1.0 if trailing_return > 0 else 0.0
        return pd.Series({self.ticker: weight})
