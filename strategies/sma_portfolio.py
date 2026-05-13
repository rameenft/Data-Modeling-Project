"""
strategies/sma_portfolio.py
----------------------------
Benchmark Strategy 1 (portfolio-level): SMA crossover.

For each stock, compute a short-window SMA (default 20d) and long-window SMA
(default 50d). Select stocks where short SMA > long SMA, then allocate equally.
"""

import pandas as pd
from strategies.base import BaseStrategy
from portfolio.constructor import uniform_weights


class SMAPortfolioStrategy(BaseStrategy):
    def __init__(self, short_window: int = 20, long_window: int = 50):
        super().__init__(name=f"SMA_Portfolio(short={short_window}, long={long_window})")
        self.short_window = short_window
        self.long_window = long_window

    def generate_weights(self, prices: pd.DataFrame, current_date: pd.Timestamp) -> pd.Series:
        history = self._no_lookahead(prices, current_date)
        all_tickers = prices.columns.tolist()

        if len(history) < self.long_window:
            return pd.Series(0.0, index=all_tickers)

        short_sma = history.iloc[-self.short_window:].mean()
        long_sma = history.iloc[-self.long_window:].mean()
        selected = [t for t in all_tickers if short_sma[t] > long_sma[t]]

        return uniform_weights(selected, all_tickers)
