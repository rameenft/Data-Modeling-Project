"""
strategies/base.py
------------------
Abstract base class for all trading strategies.

To add a new strategy:
    1. Create a new file in strategies/
    2. Subclass BaseStrategy
    3. Implement the generate_weights() method
    4. That's it — the backtesting engine handles the rest.
"""

from abc import ABC, abstractmethod
import pandas as pd


class BaseStrategy(ABC):
    """
    All strategies must inherit from this class and implement generate_weights().
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def generate_weights(
        self,
        prices: pd.DataFrame,
        current_date: pd.Timestamp,
    ) -> pd.Series:
        """
        Given all price history up to and including current_date,
        return a target allocation vector (weights).

        Parameters
        ----------
        prices : pd.DataFrame
            Full price matrix (dates x tickers), but the strategy must only
            use rows up to and including current_date (no lookahead).
        current_date : pd.Timestamp
            The current trading day.

        Returns
        -------
        pd.Series
            Index  : ticker symbols
            Values : portfolio weights (>=0, sum <= 1)
        """
        pass

    def _no_lookahead(self, prices: pd.DataFrame, current_date: pd.Timestamp) -> pd.DataFrame:
        """Helper: slice price history up to current_date (inclusive)."""
        return prices.loc[:current_date]
