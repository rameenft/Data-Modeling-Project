"""
strategies/dual_momentum.py
----------------------------
New Strategy 2 (portfolio-level): Dual-Timeframe Momentum with Vol Weighting.

Steps:
  1. Compute short-term (10d) and medium-term (60d) trailing returns for all stocks.
  2. Select stocks where BOTH are positive (momentum confirmed at two timeframes).
  3. From those candidates, take the top N by the medium-term return.
  4. Allocate inversely proportional to 20-day rolling volatility.

Rationale: requiring positive momentum at two different horizons reduces false
signals from short-term noise, selecting stocks with sustained uptrends. The
vol-weighting then tilts toward the smoother movers for a better Sharpe ratio.
"""

import pandas as pd
import numpy as np
from strategies.base import BaseStrategy
from portfolio.constructor import risk_adjusted_weights, rolling_volatility


class DualMomentumStrategy(BaseStrategy):
    def __init__(self, short_window: int = 10, long_window: int = 60,
                 top_n: int = 15, vol_window: int = 20):
        super().__init__(name=f"DualMomentum(short={short_window}, long={long_window}, N={top_n})")
        self.short_window = short_window
        self.long_window = long_window
        self.top_n = top_n
        self.vol_window = vol_window

    def generate_weights(self, prices: pd.DataFrame, current_date: pd.Timestamp) -> pd.Series:
        history = self._no_lookahead(prices, current_date)
        all_tickers = prices.columns.tolist()
        min_required = max(self.long_window + 1, self.vol_window)

        if len(history) < min_required:
            return pd.Series(0.0, index=all_tickers)

        current_prices = history.iloc[-1]

        # Short-term momentum
        past_short = history.iloc[-(self.short_window + 1)]
        short_returns = (current_prices - past_short) / past_short.replace(0, np.nan)

        # Medium-term momentum
        past_long = history.iloc[-(self.long_window + 1)]
        long_returns = (current_prices - past_long) / past_long.replace(0, np.nan)

        # Both must be positive
        dual_positive = short_returns[(short_returns > 0) & (long_returns > 0)].dropna()
        if dual_positive.empty:
            return pd.Series(0.0, index=all_tickers)

        # Rank by medium-term return among qualifying stocks
        long_returns_filtered = long_returns[dual_positive.index].dropna()
        selected = long_returns_filtered.nlargest(self.top_n).index.tolist()

        vols = rolling_volatility(history, self.vol_window)
        return risk_adjusted_weights(selected, vols, all_tickers)
