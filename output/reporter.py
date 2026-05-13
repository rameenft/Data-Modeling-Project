"""
output/reporter.py
------------------
Standardized outputs: NAV curves, metrics tables, and experiment logs.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
from datetime import datetime
from engine.backtester import BacktestResult
from metrics.performance import metrics_table


RESULTS_DIR = Path("results")


def _ensure_results_dir():
    RESULTS_DIR.mkdir(exist_ok=True)


def save_metrics_table(results: list[BacktestResult], filename: str = "metrics.csv") -> pd.DataFrame:
    """Save a metrics comparison table to CSV and return it."""
    _ensure_results_dir()
    table = metrics_table(results)
    path = RESULTS_DIR / filename
    table.to_csv(path)
    print(f"[Reporter] Metrics table saved to {path}")
    return table


def plot_nav_curves(
    results: list[BacktestResult],
    title: str = "NAV Curves",
    filename: str = "nav_curves.png",
    show: bool = False,
) -> None:
    """Plot NAV (Net Asset Value) curves for one or more strategies."""
    _ensure_results_dir()

    fig, ax = plt.subplots(figsize=(12, 5))

    for result in results:
        nav_normalised = result.nav / result.nav.iloc[0]
        ax.plot(nav_normalised.index, nav_normalised.values, label=result.strategy_name, linewidth=1.5)

    ax.set_title(title, fontsize=14)
    ax.set_ylabel("Normalised NAV (starting at 1.0)")
    ax.set_xlabel("Date")
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    plt.xticks(rotation=45)
    ax.grid(alpha=0.3)
    plt.tight_layout()

    path = RESULTS_DIR / filename
    plt.savefig(path, dpi=150)
    print(f"[Reporter] NAV curve saved to {path}")
    if show:
        plt.show()
    plt.close()


def log_experiment(
    results: list[BacktestResult],
    notes: str = "",
    filename: str = "experiment_log.txt",
) -> None:
    """Append a timestamped experiment log entry."""
    _ensure_results_dir()
    path = RESULTS_DIR / filename
    table = metrics_table(results)

    with open(path, "a") as f:
        f.write("=" * 70 + "\n")
        f.write(f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        if notes:
            f.write(f"Notes     : {notes}\n")
        f.write("\n")
        f.write(table.to_string())
        f.write("\n\n")

    print(f"[Reporter] Experiment log appended to {path}")
