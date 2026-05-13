"""
metrics/performance.py
----------------------
Standard backtesting performance metrics.
"""

import pandas as pd
import numpy as np
from engine.backtester import BacktestResult


TRADING_DAYS_PER_YEAR = 252


def compute_metrics(result: BacktestResult) -> dict:
    """
    Compute a standard set of performance metrics from a BacktestResult.

    Returns
    -------
    dict with keys:
        cumulative_return, annualized_return, annualized_volatility,
        sharpe_ratio, max_drawdown, win_rate, calmar_ratio
    """
    returns = result.returns.dropna()
    nav = result.nav.dropna()

    if len(returns) < 2:
        return {}

    # Cumulative return
    cumulative_return = nav.iloc[-1] / nav.iloc[0] - 1

    # Annualized return
    n_days = len(returns)
    n_years = n_days / TRADING_DAYS_PER_YEAR
    annualized_return = (1 + cumulative_return) ** (1 / n_years) - 1

    # Annualized volatility
    annualized_vol = returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)

    # Sharpe ratio (assume risk-free rate = 0)
    sharpe = annualized_return / annualized_vol if annualized_vol > 0 else np.nan

    # Maximum drawdown
    rolling_max = nav.cummax()
    drawdowns = (nav - rolling_max) / rolling_max
    max_drawdown = drawdowns.min()

    # Win rate (fraction of days with positive return)
    win_rate = (returns > 0).mean()

    # Calmar ratio
    calmar = annualized_return / abs(max_drawdown) if max_drawdown != 0 else np.nan

    return {
        "strategy": result.strategy_name,
        "cumulative_return": round(cumulative_return * 100, 2),       # %
        "annualized_return": round(annualized_return * 100, 2),       # %
        "annualized_volatility": round(annualized_vol * 100, 2),      # %
        "sharpe_ratio": round(sharpe, 4),
        "max_drawdown": round(max_drawdown * 100, 2),                  # %
        "win_rate": round(win_rate * 100, 2),                          # %
        "calmar_ratio": round(calmar, 4),
    }


def metrics_table(results: list[BacktestResult]) -> pd.DataFrame:
    """
    Compute metrics for a list of BacktestResults and return a summary DataFrame.
    """
    rows = [compute_metrics(r) for r in results]
    df = pd.DataFrame(rows).set_index("strategy")
    return df
