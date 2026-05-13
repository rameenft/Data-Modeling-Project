"""
strategies/topk_momentum.py
----------------------------
Benchmark Strategy 2 (portfolio-level): Top-K trailing return momentum.

Compute trailing return over `lookback` days for each stock. Select the top K
performers and allocate equally across them.
"""

import pandas as pd
from strategies.base import BaseStrategy
from portfolio.constructor import uniform_weights


class TopKMomentumStrategy(BaseStrategy):
    def __init__(self, lookback: int = 30, top_k: int = 10):
        super().__init__(name=f"TopK_Momentum(lookback={lookback}, K={top_k})")
        self.lookback = lookback
        self.top_k = top_k

    def generate_weights(self, prices: pd.DataFrame, current_date: pd.Timestamp) -> pd.Series:
        history = self._no_lookahead(prices, current_date)
        all_tickers = prices.columns.tolist()

        if len(history) < self.lookback + 1:
            return pd.Series(0.0, index=all_tickers)

        past_prices = history.iloc[-(self.lookback + 1)]
        current_prices = history.iloc[-1]
        trailing_returns = (current_prices - past_prices) / past_prices.replace(0, float("nan"))
        trailing_returns = trailing_returns.dropna()

        selected = trailing_returns.nlargest(self.top_k).index.tolist()
        return uniform_weights(selected, all_tickers)
