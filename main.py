"""
main.py
-------
Entry point for the INDENG 231 backtesting simulation system.

Usage:
    python main.py [--deliverable {3,4,5,all}]

Defaults to running all deliverables.
"""

import argparse
import pandas as pd
from data.loader import load_prices
from engine.backtester import Backtester
from output.reporter import save_metrics_table, plot_nav_curves, log_experiment
import config


def run_deliverable3(backtester: Backtester) -> None:
    """Single-stock strategy evaluation on config.SINGLE_STOCK."""
    from strategies.momentum import MomentumStrategy
    from strategies.mean_reversion import MeanReversionStrategy
    from strategies.macd import MACDStrategy
    from strategies.bollinger_band import BollingerBandStrategy
    from strategies.rsi_strategy import RSIStrategy

    print(f"\n{'='*60}")
    print(f"  Deliverable 3: Single-Stock Strategies ({config.SINGLE_STOCK})")
    print(f"{'='*60}")

    strategies = [
        MomentumStrategy(lookback=config.MOMENTUM_LOOKBACK, ticker=config.SINGLE_STOCK),
        MeanReversionStrategy(lookback=config.MEAN_REVERSION_LOOKBACK, ticker=config.SINGLE_STOCK),
        MACDStrategy(ticker=config.SINGLE_STOCK),
        BollingerBandStrategy(ticker=config.SINGLE_STOCK),
        RSIStrategy(ticker=config.SINGLE_STOCK),
    ]

    results = []
    for s in strategies:
        print(f"   Running: {s.name}")
        results.append(backtester.run(s))

    table = save_metrics_table(results, filename="d3_single_stock_metrics.csv")
    plot_nav_curves(results, title=f"D3: Single-Stock Strategies — {config.SINGLE_STOCK}",
                   filename="d3_nav_curves.png")
    log_experiment(results, notes=f"D3 single stock: {config.SINGLE_STOCK}")

    print("\n--- D3 Performance Summary ---")
    print(table.to_string())


def run_deliverable4(backtester: Backtester) -> None:
    """Portfolio-level backtesting: uniform vs risk-adjusted weighting."""
    from strategies.sma_portfolio import SMAPortfolioStrategy
    from strategies.topk_momentum import TopKMomentumStrategy
    from strategies.base import BaseStrategy
    from portfolio.constructor import risk_adjusted_weights, rolling_volatility

    print(f"\n{'='*60}")
    print("  Deliverable 4: Portfolio Backtesting")
    print(f"{'='*60}")

    class TopKRiskAdjusted(BaseStrategy):
        """Top-K momentum with inverse-volatility weighting (risk-adjusted portfolio)."""
        def __init__(self, lookback: int = 30, top_k: int = 10, vol_window: int = 20):
            super().__init__(name=f"TopK_RiskAdjusted(K={top_k})")
            self.lookback = lookback
            self.top_k = top_k
            self.vol_window = vol_window

        def generate_weights(self, prices, current_date):
            import numpy as np
            history = self._no_lookahead(prices, current_date)
            all_tickers = prices.columns.tolist()
            if len(history) < self.lookback + 1:
                return pd.Series(0.0, index=all_tickers)
            past = history.iloc[-(self.lookback + 1)]
            curr = history.iloc[-1]
            ret = (curr - past) / past.replace(0, float("nan"))
            selected = ret.dropna().nlargest(self.top_k).index.tolist()
            vols = rolling_volatility(history, self.vol_window)
            return risk_adjusted_weights(selected, vols, all_tickers)

    strategies = [
        SMAPortfolioStrategy(short_window=config.SMA_SHORT, long_window=config.SMA_LONG),
        TopKMomentumStrategy(lookback=config.TRAILING_RETURN_LOOKBACK, top_k=config.TOP_K),
        TopKRiskAdjusted(lookback=config.TRAILING_RETURN_LOOKBACK, top_k=config.TOP_K,
                         vol_window=config.VOLATILITY_LOOKBACK),
    ]

    results = []
    for s in strategies:
        print(f"   Running: {s.name}")
        results.append(backtester.run(s))

    table = save_metrics_table(results, filename="d4_portfolio_metrics.csv")
    plot_nav_curves(results, title="D4: Portfolio Strategies — Uniform vs Risk-Adjusted",
                   filename="d4_nav_curves.png")
    log_experiment(results, notes="D4 portfolio backtesting")

    print("\n--- D4 Performance Summary ---")
    print(table.to_string())


def run_deliverable5(backtester: Backtester) -> None:
    """Compare benchmark strategies vs two new strategies by Sharpe ratio."""
    from strategies.sma_portfolio import SMAPortfolioStrategy
    from strategies.topk_momentum import TopKMomentumStrategy
    from strategies.risk_adjusted_momentum import RiskAdjustedMomentumStrategy
    from strategies.market_timed_momentum import MarketTimedMomentumStrategy

    print(f"\n{'='*60}")
    print("  Deliverable 5: New Strategies vs Benchmarks")
    print(f"{'='*60}")

    strategies = [
        SMAPortfolioStrategy(short_window=config.SMA_SHORT, long_window=config.SMA_LONG),
        TopKMomentumStrategy(lookback=config.TRAILING_RETURN_LOOKBACK, top_k=config.TOP_K),
        RiskAdjustedMomentumStrategy(lookback=config.TRAILING_RETURN_LOOKBACK,
                                     top_k=15, vol_window=config.VOLATILITY_LOOKBACK),
        MarketTimedMomentumStrategy(lookback=config.TRAILING_RETURN_LOOKBACK,
                                    top_k=15, market_window=90,
                                    vol_window=config.VOLATILITY_LOOKBACK),
    ]

    results = []
    for s in strategies:
        print(f"   Running: {s.name}")
        results.append(backtester.run(s))

    table = save_metrics_table(results, filename="d5_benchmark_vs_new_metrics.csv")
    plot_nav_curves(results, title="D5: Benchmark vs New Strategies",
                   filename="d5_nav_curves.png")
    log_experiment(results, notes="D5 benchmark vs new strategies")

    print("\n--- D5 Performance Summary (Sharpe Ratio Focus) ---")
    sharpe_cols = ["sharpe_ratio", "annualized_return", "annualized_volatility", "max_drawdown"]
    available = [c for c in sharpe_cols if c in table.columns]
    print(table[available].to_string())


def main():
    parser = argparse.ArgumentParser(description="INDENG 231 Backtesting System")
    parser.add_argument("--deliverable", choices=["3", "4", "5", "all"], default="all")
    args = parser.parse_args()

    print("=" * 60)
    print("  INDENG 231 Backtesting System")
    print("=" * 60)

    print(f"\n[1/2] Loading price data from {config.DATA_PATH} ...")
    prices = load_prices(config.DATA_PATH)
    print(f"      {len(prices)} trading days x {len(prices.columns)} stocks")
    print(f"      Date range: {prices.index[0].date()} → {prices.index[-1].date()}")

    backtester = Backtester(
        prices=prices,
        initial_capital=config.INITIAL_CAPITAL,
        start_date=config.START_DATE,
        end_date=config.END_DATE,
    )

    print(f"\n[2/2] Running backtests (deliverable={args.deliverable}) ...")

    d = args.deliverable
    if d in ("3", "all"):
        run_deliverable3(backtester)
    if d in ("4", "all"):
        run_deliverable4(backtester)
    if d in ("5", "all"):
        run_deliverable5(backtester)

    print("\nDone. All results saved to results/")


if __name__ == "__main__":
    main()
