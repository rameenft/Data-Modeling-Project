"""
config.py
---------
Central configuration for the backtesting system.
Modify parameters here rather than inside individual modules.
"""

from pathlib import Path

# --- Data ---
DATA_PATH = Path("nasdaq100_daily_5y.csv")

# --- Backtest ---
INITIAL_CAPITAL = 1.0          # normalised starting portfolio value
START_DATE = None               # None = use first date in dataset
END_DATE = None                 # None = use last date in dataset

# --- Strategy parameters ---
MOMENTUM_LOOKBACK = 20          # days for momentum signal
MEAN_REVERSION_LOOKBACK = 20   # days for mean reversion signal
SMA_SHORT = 20                  # short moving average window
SMA_LONG = 50                   # long moving average window
TRAILING_RETURN_LOOKBACK = 30   # lookback for benchmark strategy 2
TOP_K = 10                      # number of top stocks for momentum portfolio
VOLATILITY_LOOKBACK = 20        # rolling window for risk-adjusted weighting

# --- Single stock for Deliverable 3 ---
SINGLE_STOCK = "AAPL"
