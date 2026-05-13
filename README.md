# Backtesting Simulation for Trading Strategies

INDENG 231 — Data Modeling, UC Berkeley, Spring 2026

---

## Overview

This project builds a daily-close backtesting simulation system on five years of Nasdaq-100 constituent data (April 2021 to April 2026, 1,255 trading days, 101 stocks). Strategies are evaluated under strict assumptions: no lookahead bias, no short selling, no leverage, no intraday trading, and no transaction costs. Starting capital is normalized to 1.0 for comparability.

The project is structured across three deliverables:

**Deliverable 3 — Single-stock strategy evaluation (AAPL)**

Five classic strategies are tested on Apple: momentum, mean reversion, MACD, Bollinger Bands, and RSI. Momentum is the strongest performer (Sharpe 0.66, cumulative return 73%), consistent with the documented momentum effect in large-cap equities. Mean-reversion and RSI strategies underperform because they repeatedly attempt to exit a sustained uptrend, resulting in low win rates and high drawdowns despite modest returns.

**Deliverable 4 — Portfolio-level backtesting**

The simulation scales to the full 101-stock universe using two portfolio construction methods: equal weighting and inverse-volatility weighting. Three strategies are tested: an SMA crossover portfolio (Sharpe 0.61), top-10 momentum with equal weighting (Sharpe 1.01, cumulative return 239%), and top-10 momentum with risk-adjusted weighting (Sharpe 0.83). Cross-sectional momentum with equal weighting achieves the best risk-adjusted performance, capturing the AI-driven Nasdaq rally of 2023-2025.

**Deliverable 5 — New strategies vs benchmarks**

Two new strategies are designed to beat both benchmark Sharpe ratios (0.61 and 1.01). Risk-adjusted momentum with an RSI overbought filter reaches Sharpe 1.14 by avoiding overextended stocks and concentrating capital in steadier climbers. Market-timed momentum achieves Sharpe 1.35 with a maximum drawdown of only -11.84% by moving to 100% cash when the 90-day broad-market trend is negative, successfully avoiding the 2022 rate-hike bear market while staying invested during bull runs.

---

## Project Structure

```
.
├── data/
│   └── loader.py               reads CSV, pivots to wide price matrix (dates x tickers)
├── engine/
│   └── backtester.py           core simulation loop, NAV tracking, weight history
├── strategies/
│   ├── base.py                 BaseStrategy abstract class
│   ├── momentum.py
│   ├── mean_reversion.py
│   ├── macd.py
│   ├── bollinger_band.py
│   ├── rsi_strategy.py
│   ├── sma_portfolio.py
│   ├── topk_momentum.py
│   ├── risk_adjusted_momentum.py
│   └── market_timed_momentum.py
├── portfolio/
│   └── constructor.py          uniform_weights(), risk_adjusted_weights()
├── metrics/
│   └── performance.py          Sharpe, drawdown, Calmar, win rate
├── output/
│   └── reporter.py             saves CSV results, NAV curve plots, experiment logs
├── main.py                     entry point
├── config.py                   strategy parameters
├── nasdaq100_daily_5y.csv      price data
├── requirements.txt
└── INDENG231_Project1_Report.pdf
```

---

## Setup

```bash
pip install pandas numpy matplotlib
```

---

## Usage

```bash
python main.py                    # run all deliverables
python main.py --deliverable 3    # single-stock strategies (AAPL)
python main.py --deliverable 4    # portfolio strategies
python main.py --deliverable 5    # new strategies vs benchmarks
```

Results are saved to `output/` as CSV metrics tables and NAV curve plots.

---

## Performance Summary

| Strategy | Ann. Return | Sharpe | Max Drawdown |
|---|---|---|---|
| Momentum (AAPL, 20d) | 11.66% | 0.66 | -19.75% |
| SMA Portfolio | 11.51% | 0.61 | -37.71% |
| TopK Momentum (K=10, equal weight) | 27.79% | 1.01 | -43.25% |
| Risk-Adjusted Momentum + RSI Filter | 25.05% | 1.14 | -39.69% |
| Market-Timed Momentum | 24.70% | 1.35 | -11.84% |
