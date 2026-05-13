"""
strategies/volatility_managed_momentum.py
------------------------------------------
New Strategy 2 (portfolio-level): Volatility-Managed Momentum.

Steps:
  1. Select the top N stocks by 30-day trailing return (same signal as TopK Momentum).
  2. Compute an inverse-vol weight vector across the selected stocks.
  3. Scale the TOTAL portfolio exposure by the inverse of recent realized portfolio
     volatility, targeting a fixed annualized volatility level (default 15%).
     When the market is turbulent, this pulls capital into cash automatically.

Rationale (Moreira & Muir, 2017): scaling a momentum portfolio by the inverse of
its lagged realized variance consistently improves Sharpe ratio by reducing
allocation during high-vol drawdown periods while staying invested in calm regimes.
"""

import pandas as pd
import numpy as np
from strategies.base import BaseStrategy
from portfolio.constructor import risk_adjusted_weights, rolling_volatility


class VolatilityManagedMomentumStrategy(BaseStrategy):
    def __init__(self, lookback: int = 30, top_n: int = 15, vol_window: int = 20,
                 target_vol: float = 0.15):
        super().__init__(name=f"VolManaged_Momentum(N={top_n}, target_vol={int(target_vol*100)}%)")
        self.lookback = lookback
        self.top_n = top_n
        self.vol_window = vol_window
        self.target_vol = target_vol  # annualized

    def generate_weights(self, prices: pd.DataFrame, current_date: pd.Timestamp) -> pd.Series:
        history = self._no_lookahead(prices, current_date)
        all_tickers = prices.columns.tolist()
        min_required = max(self.lookback + 1, self.vol_window + 1)

        if len(history) < min_required:
            return pd.Series(0.0, index=all_tickers)

        # Step 1: top-N momentum signal
        past_prices = history.iloc[-(self.lookback + 1)]
        current_prices = history.iloc[-1]
        trailing_returns = (current_prices - past_prices) / past_prices.replace(0, np.nan)
        selected = trailing_returns.dropna().nlargest(self.top_n).index.tolist()

        # Step 2: inverse-vol weights across selected stocks
        vols = rolling_volatility(history, self.vol_window)
        base_weights = risk_adjusted_weights(selected, vols, all_tickers)

        # Step 3: scale total exposure by lagged realized portfolio volatility
        # Approximate portfolio daily returns using base weights and recent price history
        recent_returns = history[selected].pct_change().iloc[-self.vol_window:].fillna(0)
        port_weights_vec = base_weights[selected].values
        port_daily_returns = recent_returns.values @ port_weights_vec
        realized_vol = port_daily_returns.std() * np.sqrt(252)

        if realized_vol > 0:
            scale = min(self.target_vol / realized_vol, 1.0)
        else:
            scale = 1.0

        return base_weights * scale
