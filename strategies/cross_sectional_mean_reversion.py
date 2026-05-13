"""
strategies/cross_sectional_mean_reversion.py
---------------------------------------------
New Strategy 2 (portfolio-level): Cross-Sectional Mean Reversion with Vol Weighting.

Steps:
  1. Compute the 5-day return for every stock.
  2. Compute the cross-sectional z-score of those returns (mean and std across stocks).
  3. Select stocks whose z-score < -z_threshold (most underperforming vs. peers today).
  4. Allocate inversely proportional to 20-day rolling volatility.

Rationale: stocks that have underperformed their peers in the short term tend to
revert toward the cross-sectional mean, especially in large-cap indices where
idiosyncratic shocks are often transient.
"""

import pandas as pd
import numpy as np
from strategies.base import BaseStrategy
from portfolio.constructor import risk_adjusted_weights, rolling_volatility


class CrossSectionalMeanReversionStrategy(BaseStrategy):
    def __init__(self, short_window: int = 5, z_threshold: float = 1.0,
                 top_n: int = 15, vol_window: int = 20):
        super().__init__(name=f"CrossSection_MeanReversion(z<-{z_threshold}, N={top_n})")
        self.short_window = short_window
        self.z_threshold = z_threshold
        self.top_n = top_n
        self.vol_window = vol_window

    def generate_weights(self, prices: pd.DataFrame, current_date: pd.Timestamp) -> pd.Series:
        history = self._no_lookahead(prices, current_date)
        all_tickers = prices.columns.tolist()
        min_required = max(self.short_window + 1, self.vol_window)

        if len(history) < min_required:
            return pd.Series(0.0, index=all_tickers)

        # Step 1 & 2: cross-sectional z-scores of short-term returns
        past_prices = history.iloc[-(self.short_window + 1)]
        current_prices = history.iloc[-1]
        short_returns = (current_prices - past_prices) / past_prices.replace(0, np.nan)
        short_returns = short_returns.dropna()

        cross_mean = short_returns.mean()
        cross_std = short_returns.std()
        if cross_std == 0:
            return pd.Series(0.0, index=all_tickers)

        z_scores = (short_returns - cross_mean) / cross_std

        # Step 3: select most underperforming (lowest z-scores)
        candidates = z_scores[z_scores < -self.z_threshold]
        if candidates.empty:
            return pd.Series(0.0, index=all_tickers)

        selected = candidates.nsmallest(self.top_n).index.tolist()

        # Step 4: inverse vol weighting
        vols = rolling_volatility(history, self.vol_window)
        return risk_adjusted_weights(selected, vols, all_tickers)
