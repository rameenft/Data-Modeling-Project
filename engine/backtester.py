"""
engine/backtester.py
--------------------
Core backtesting loop. Simulates daily close trading strategy execution.

Rules enforced:
  - No short selling  (weights >= 0)
  - No leverage       (sum of weights <= 1)
  - No lookahead      (strategy only sees prices up to current day)
  - Trades execute at closing price of each day
"""

import pandas as pd
import numpy as np
from strategies.base import BaseStrategy


class BacktestResult:
    """Container for all outputs of a single backtest run."""

    def __init__(
        self,
        strategy_name: str,
        nav: pd.Series,
        weights_history: pd.DataFrame,
        returns: pd.Series,
    ):
        self.strategy_name = strategy_name
        self.nav = nav                          # Net Asset Value over time
        self.weights_history = weights_history  # daily portfolio weights
        self.returns = returns                  # daily portfolio returns


class Backtester:
    """
    Runs a backtesting simulation for a given strategy over a price matrix.

    Parameters
    ----------
    prices : pd.DataFrame
        Dates x tickers closing price matrix.
    initial_capital : float
        Starting portfolio value (default: 1.0, i.e. normalised).
    start_date : str or pd.Timestamp, optional
        First date to begin trading. Defaults to the first date in prices.
    end_date : str or pd.Timestamp, optional
        Last date to trade. Defaults to the last date in prices.
    """

    def __init__(
        self,
        prices: pd.DataFrame,
        initial_capital: float = 1.0,
        start_date=None,
        end_date=None,
    ):
        self.prices = prices
        self.initial_capital = initial_capital

        self.start_date = pd.Timestamp(start_date) if start_date else prices.index[0]
        self.end_date = pd.Timestamp(end_date) if end_date else prices.index[-1]

        self.trading_days = prices.loc[self.start_date:self.end_date].index

    def run(self, strategy: BaseStrategy) -> BacktestResult:
        """
        Execute the backtest for the given strategy.

        Returns
        -------
        BacktestResult
        """
        tickers = self.prices.columns.tolist()
        n_days = len(self.trading_days)

        nav = pd.Series(index=self.trading_days, dtype=float)
        weights_history = pd.DataFrame(index=self.trading_days, columns=tickers, dtype=float)
        portfolio_returns = pd.Series(index=self.trading_days, dtype=float)

        nav.iloc[0] = self.initial_capital
        portfolio_returns.iloc[0] = 0.0
        current_weights = pd.Series(0.0, index=tickers)

        for i, date in enumerate(self.trading_days):
            # --- Generate target weights (no lookahead enforced inside strategy) ---
            target_weights = strategy.generate_weights(self.prices, date)

            # --- Enforce constraints ---
            target_weights = target_weights.reindex(tickers).fillna(0.0)
            target_weights = target_weights.clip(lower=0.0)
            total = target_weights.sum()
            if total > 1.0:
                target_weights = target_weights / total  # normalise to sum=1

            weights_history.loc[date] = target_weights

            # --- Compute portfolio return for next day ---
            if i + 1 < n_days:
                next_date = self.trading_days[i + 1]

                # Daily returns of each stock
                today_prices = self.prices.loc[date, tickers]
                next_prices = self.prices.loc[next_date, tickers]
                stock_returns = (next_prices - today_prices) / today_prices
                stock_returns = stock_returns.fillna(0.0)

                # Portfolio return = weighted sum of stock returns
                port_return = (target_weights * stock_returns).sum()
                portfolio_returns.iloc[i + 1] = port_return
                nav.iloc[i + 1] = nav.iloc[i] * (1 + port_return)

            current_weights = target_weights

        return BacktestResult(
            strategy_name=strategy.name,
            nav=nav,
            weights_history=weights_history,
            returns=portfolio_returns,
        )
