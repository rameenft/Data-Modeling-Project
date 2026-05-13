"""Generate INDENG231_Project1_Report.pdf using reportlab."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

OUTPUT = "INDENG231_Project1_Report.pdf"

def build():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        leftMargin=1*inch, rightMargin=1*inch,
        topMargin=1*inch, bottomMargin=1*inch,
    )

    base = getSampleStyleSheet()

    title_style = ParagraphStyle("ReportTitle", parent=base["Title"],
        fontSize=16, leading=20, spaceAfter=6, alignment=TA_CENTER)
    subtitle_style = ParagraphStyle("Subtitle", parent=base["Normal"],
        fontSize=11, leading=14, spaceAfter=16, alignment=TA_CENTER, textColor=colors.grey)
    h1 = ParagraphStyle("H1", parent=base["Heading1"],
        fontSize=13, leading=16, spaceBefore=18, spaceAfter=6,
        textColor=colors.HexColor("#1a3a5c"))
    h2 = ParagraphStyle("H2", parent=base["Heading2"],
        fontSize=11, leading=14, spaceBefore=10, spaceAfter=4,
        textColor=colors.HexColor("#2c5f8a"))
    body = ParagraphStyle("Body", parent=base["Normal"],
        fontSize=10, leading=14, spaceAfter=6, alignment=TA_JUSTIFY)
    bullet = ParagraphStyle("Bullet", parent=base["Normal"],
        fontSize=10, leading=14, spaceAfter=3, leftIndent=16,
        bulletIndent=4)
    code_style = ParagraphStyle("Code", parent=base["Normal"],
        fontSize=9, leading=13, fontName="Courier",
        backColor=colors.HexColor("#f4f4f4"), leftIndent=12, rightIndent=12,
        spaceAfter=6)

    BLUE = colors.HexColor("#1a3a5c")
    LIGHT_BLUE = colors.HexColor("#dce8f5")
    MID_BLUE = colors.HexColor("#2c5f8a")

    def table_style(header_bg=BLUE):
        return TableStyle([
            ("BACKGROUND", (0,0), (-1,0), header_bg),
            ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
            ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE",   (0,0), (-1,0), 8),
            ("ALIGN",      (0,0), (-1,-1), "CENTER"),
            ("ALIGN",      (0,1), (0,-1), "LEFT"),
            ("FONTNAME",   (0,1), (-1,-1), "Helvetica"),
            ("FONTSIZE",   (0,1), (-1,-1), 8),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT_BLUE]),
            ("GRID",       (0,0), (-1,-1), 0.4, colors.HexColor("#aaaaaa")),
            ("TOPPADDING", (0,0), (-1,-1), 4),
            ("BOTTOMPADDING", (0,0), (-1,-1), 4),
            ("LEFTPADDING", (0,0), (-1,-1), 5),
            ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ])

    story = []

    # ── Title page ──────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("INDENG 231 — Data Modeling", subtitle_style))
    story.append(Paragraph("Course Project 1", subtitle_style))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph(
        "Building a Backtesting Simulation<br/>for Trading Strategies", title_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(HRFlowable(width="100%", thickness=1.5, color=BLUE))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Nasdaq-100 Daily Data · April 2021 – April 2026", subtitle_style))
    story.append(Spacer(1, 0.4*inch))

    # ── Section 1 ────────────────────────────────────────────────────────────
    story.append(Paragraph("1. System Overview and Assumptions", h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=MID_BLUE))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "This report describes the design, implementation, and experimental results of a daily "
        "close trading strategy backtesting simulation system built on five years of Nasdaq-100 "
        "constituent stock data (April 2021 – April 2026, 1,255 trading days, 101 stocks).",
        body))
    story.append(Paragraph("The system enforces the following assumptions throughout all experiments:", body))
    for b in [
        "<b>No lookahead bias:</b> strategies may only use price data up to and including the current trading day.",
        "<b>No short selling:</b> all portfolio weights are constrained to be non-negative.",
        "<b>No leverage:</b> the sum of all weights is at most 1.0; any remainder is held as cash.",
        "<b>No intraday trading:</b> all decisions and executions occur at the daily closing price.",
        "<b>Frictionless execution:</b> no transaction costs or slippage are modeled.",
        "<b>Normalized capital:</b> starting portfolio value is 1.0 for comparability across strategies.",
    ]:
        story.append(Paragraph(f"• {b}", bullet))

    # ── Section 2 ────────────────────────────────────────────────────────────
    story.append(Paragraph("2. System Architecture and Module Interaction", h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=MID_BLUE))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "The system is organized into six modules that interact in a clean pipeline. "
        "Each module has a single responsibility, making it easy to extend or replace "
        "individual components without touching the rest of the codebase.", body))

    modules = [
        ("data/loader.py", "Reads nasdaq100_daily_5y.csv, pivots from long format (ticker, date, close) to a wide price matrix (dates x tickers), and sorts by date."),
        ("engine/backtester.py", "Core simulation loop. For each trading day t, calls strategy.generate_weights(prices, t), enforces constraints, then computes portfolio return as the dot product of weights and next-day stock returns. Tracks NAV, daily returns, and weight history."),
        ("strategies/base.py", "Defines BaseStrategy, an abstract class with a single required method generate_weights(prices, current_date). All strategies subclass this. A _no_lookahead() helper slices history to the current date. Adding a new strategy requires no changes to any other module."),
        ("portfolio/constructor.py", "Provides uniform_weights() (equal allocation) and risk_adjusted_weights() (inverse-volatility weighting), plus rolling_volatility() for computing annualized rolling vol."),
        ("metrics/performance.py", "Computes cumulative return, annualized return, annualized volatility, Sharpe ratio, maximum drawdown, win rate, and Calmar ratio from a BacktestResult object."),
        ("output/reporter.py", "Saves metrics tables to CSV, plots NAV curves as PNG files, and appends timestamped experiment logs to a text file."),
        ("main.py", "Entry point. Loads data, instantiates Backtester, imports strategies, runs backtests, and saves all outputs. Accepts --deliverable {3,4,5,all} to run specific experiment sets."),
    ]
    for mod, desc in modules:
        story.append(Paragraph(f"<b>{mod}</b>", h2))
        story.append(Paragraph(desc, body))

    story.append(Paragraph("Module interaction flow:", body))
    story.append(Paragraph(
        "main.py  →  data/loader.py  →  engine/backtester.py  ↔  strategies/*  →  metrics/performance.py  →  output/reporter.py",
        code_style))

    # ── Section 3 ────────────────────────────────────────────────────────────
    story.append(Paragraph("3. Performance Metrics", h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=MID_BLUE))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "The following metrics are used to evaluate all strategies. A strategy is considered "
        "strong if it achieves a high Sharpe ratio with a manageable maximum drawdown — raw "
        "returns alone are insufficient because higher returns often come with "
        "disproportionately higher risk.", body))
    metrics_data = [
        ["Metric", "Definition"],
        ["Cumulative Return (%)", "Total portfolio growth over the full period."],
        ["Annualized Return (%)", "Geometric annualized return, assuming 252 trading days/year."],
        ["Annualized Volatility (%)", "Std. dev. of daily returns scaled to annual."],
        ["Sharpe Ratio", "Ann. return / ann. volatility (risk-free rate = 0). Above 1.0 is strong."],
        ["Maximum Drawdown (%)", "Largest peak-to-trough NAV decline. Measures downside risk."],
        ["Win Rate (%)", "Fraction of trading days with positive portfolio return."],
        ["Calmar Ratio", "Ann. return / |max drawdown|. Return per unit of drawdown risk."],
    ]
    t = Table(metrics_data, colWidths=[2.1*inch, 4.3*inch])
    t.setStyle(table_style())
    story.append(t)

    # ── Section 4 ────────────────────────────────────────────────────────────
    story.append(Paragraph("4. Deliverable 3 — Single-Stock Strategy Evaluation (AAPL)", h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=MID_BLUE))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Five strategies were tested on Apple Inc. (AAPL) over the full five-year period "
        "(April 2021 – April 2026).", body))

    story.append(Paragraph("4.1 Strategy Descriptions", h2))
    strats = [
        ("Momentum (lookback=20)", "Holds AAPL if its 20-day trailing return is positive; otherwise holds cash. Captures short-term price persistence."),
        ("Mean Reversion (lookback=20)", "Computes a 20-day rolling z-score of the price. Buys when z-score < -1.0 (price unusually low), expecting reversion to the mean."),
        ("MACD (12, 26, 9)", "MACD line = EMA(12) - EMA(26). Signal line = EMA(9) of MACD. Holds long when MACD is above the signal line (bullish crossover)."),
        ("Bollinger Band (window=20)", "Buys when price drops below the lower band (mean - 2*std). Exits when price rises above the upper band (mean + 2*std)."),
        ("RSI (period=14)", "Enters a long position when RSI falls below 30 (oversold). Exits when RSI exceeds 70 (overbought)."),
    ]
    for name, desc in strats:
        story.append(Paragraph(f"<b>{name}:</b> {desc}", bullet))

    story.append(Spacer(1, 8))
    story.append(Paragraph("4.2 Results", h2))
    d3_data = [
        ["Strategy", "Cum. Return (%)", "Ann. Return (%)", "Ann. Vol (%)", "Sharpe", "Max DD (%)", "Win Rate (%)", "Calmar"],
        ["Momentum (20d)",     "73.20", "11.66", "17.55", "0.664", "-19.75", "29.88", "0.590"],
        ["Mean Reversion (20d)","42.78","7.41",  "16.04", "0.462", "-23.61", "11.47", "0.314"],
        ["MACD (12,26,9)",     "57.50", "9.55",  "17.02", "0.561", "-20.89", "25.58", "0.457"],
        ["Bollinger Band (20d)","48.33","8.24",  "20.66", "0.399", "-30.22", "22.79", "0.273"],
        ["RSI (14)",           "30.39", "5.47",  "19.24", "0.284", "-30.22", "20.80", "0.181"],
    ]
    t3 = Table(d3_data, colWidths=[1.45*inch, 0.75*inch, 0.75*inch, 0.7*inch, 0.6*inch, 0.75*inch, 0.75*inch, 0.65*inch])
    t3.setStyle(table_style())
    story.append(t3)

    story.append(Spacer(1, 8))
    story.append(Paragraph("4.3 Analysis", h2))
    story.append(Paragraph(
        "<b>Momentum</b> is the strongest performer on all risk-adjusted metrics (Sharpe 0.664, "
        "Calmar 0.590). This is consistent with the documented momentum effect in large-cap "
        "equities: stocks with recent positive price trends tend to continue in that direction "
        "over short horizons.", body))
    story.append(Paragraph(
        "<b>Mean Reversion</b> achieves the lowest volatility (16.04%) but a lower Sharpe (0.462) "
        "and a very low win rate (11.47%), because it spends most of the time in cash waiting "
        "for dips that may not materialize in a trending bull market.", body))
    story.append(Paragraph(
        "<b>MACD</b> performs between the two extremes, smoothing the momentum signal with EMAs "
        "to reduce whipsaw trades.", body))
    story.append(Paragraph(
        "<b>Bollinger Band and RSI</b> are the weakest performers. Both are contrarian strategies "
        "that struggle in sustained uptrends: they repeatedly exit positions expecting a reversal, "
        "resulting in the highest drawdowns (-30.22%) despite the lowest returns. RSI's Sharpe of "
        "0.284 highlights the pitfall of applying mean-reversion logic to a structurally "
        "trending stock.", body))

    # ── Section 5 ────────────────────────────────────────────────────────────
    story.append(Paragraph("5. Deliverable 4 — Portfolio-Level Backtesting", h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=MID_BLUE))
    story.append(Spacer(1, 4))

    story.append(Paragraph("5.1 Portfolio Construction Methods", h2))
    story.append(Paragraph(
        "<b>Uniform Weighting:</b> selected stocks receive equal allocation (1/N each). "
        "Simple and well-diversified, but ignores differences in risk across stocks.", body))
    story.append(Paragraph(
        "<b>Risk-Adjusted (Inverse Volatility) Weighting:</b> each selected stock is weighted "
        "inversely proportional to its 20-day rolling annualized volatility. Stocks with "
        "lower volatility receive higher allocations, reducing the influence of highly "
        "volatile names.", body))

    story.append(Paragraph("5.2 Strategies Tested", h2))
    story.append(Paragraph(
        "<b>SMA Portfolio:</b> selects all stocks where the 20-day SMA is above the 50-day SMA "
        "(uptrend filter). Allocates equally across selected stocks.", body))
    story.append(Paragraph(
        "<b>TopK Momentum — Uniform:</b> ranks all 101 stocks by 30-day trailing return, selects "
        "the top 10, and allocates equally.", body))
    story.append(Paragraph(
        "<b>TopK Momentum — Risk-Adjusted:</b> same top-10 momentum selection, but uses "
        "inverse-volatility weighting instead of equal weight.", body))

    story.append(Paragraph("5.3 Results", h2))
    d4_data = [
        ["Strategy", "Cum. Return (%)", "Ann. Return (%)", "Ann. Vol (%)", "Sharpe", "Max DD (%)", "Win Rate (%)", "Calmar"],
        ["SMA Portfolio (uniform)",        "72.00",  "11.51", "18.97", "0.606", "-37.71", "51.63", "0.305"],
        ["TopK Momentum (uniform, K=10)",  "239.09", "27.79", "27.59", "1.007", "-43.25", "52.51", "0.642"],
        ["TopK Momentum (risk-adj, K=10)", "158.27", "20.99", "25.43", "0.825", "-44.00", "52.19", "0.477"],
    ]
    t4 = Table(d4_data, colWidths=[1.85*inch, 0.75*inch, 0.75*inch, 0.7*inch, 0.6*inch, 0.7*inch, 0.75*inch, 0.6*inch])
    t4.setStyle(table_style())
    story.append(t4)

    story.append(Spacer(1, 8))
    story.append(Paragraph("5.4 Analysis", h2))
    story.append(Paragraph(
        "<b>TopK Momentum with uniform weighting</b> achieves the highest cumulative return (239%) "
        "and the best Sharpe (1.007), demonstrating that cross-sectional momentum is a powerful "
        "signal in the Nasdaq-100. The top-10 stocks consistently captured the market's strongest "
        "performers (e.g., NVDA, META, MSTR during the AI-driven bull run of 2023–2025).", body))
    story.append(Paragraph(
        "<b>Risk-adjusted weighting</b> reduces volatility from 27.59% to 25.43%, but also reduces "
        "returns more proportionally, resulting in a lower Sharpe (0.825). This occurs because "
        "the highest-momentum stocks in this dataset are often also the highest-volatility stocks "
        "— downweighting them reduces both risk and return simultaneously.", body))
    story.append(Paragraph(
        "<b>SMA Portfolio</b> has a lower Sharpe (0.606) because the SMA crossover signal is slower "
        "to respond and selects a larger, more diluted set of stocks. Its max drawdown of -37.71% "
        "is lower than TopK strategies, making it more suitable for risk-averse portfolios.", body))

    # ── Section 6 ────────────────────────────────────────────────────────────
    story.append(Paragraph("6. Deliverable 5 — New Strategies vs Benchmark Strategies", h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=MID_BLUE))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "The objective is to develop two new strategies that beat both benchmarks on Sharpe ratio. "
        "Benchmark 1 (SMA Portfolio) has Sharpe 0.606. Benchmark 2 (TopK Momentum, K=10) has "
        "Sharpe 1.007.", body))

    story.append(Paragraph("6.1 New Strategy 1: Risk-Adjusted Momentum with RSI Filter", h2))
    story.append(Paragraph(
        "<b>Description:</b> Computes 30-day trailing return for all 101 stocks. Filters out any "
        "stock with RSI above 70 (overbought — avoiding stocks vulnerable to reversals after "
        "large runs). From the remaining stocks, selects the top 15 by momentum and allocates "
        "using inverse-volatility weighting.", body))
    story.append(Paragraph(
        "<b>Rationale:</b> The RSI filter adds a quality screen on top of momentum, avoiding "
        "crowded trades in overextended stocks. Inverse-vol weighting then allocates more to "
        "the smoother, steadier winners, improving the risk-adjusted return.", body))

    story.append(Paragraph("6.2 New Strategy 2: Market-Timed Momentum", h2))
    story.append(Paragraph(
        "<b>Description:</b> First checks the broad-market trend by computing the equal-weighted "
        "return of all 101 Nasdaq-100 stocks over the past 90 days. If this return is negative "
        "(broad market in a downtrend), the strategy holds 100% cash. Otherwise, selects the "
        "top 15 stocks by 30-day momentum and allocates using inverse-volatility weighting.", body))
    story.append(Paragraph(
        "<b>Rationale:</b> Based on absolute momentum theory (Antonacci, 2012), a negative "
        "broad-market trend is a strong signal to exit risky assets entirely. This dramatically "
        "reduces drawdowns during market-wide selloffs (e.g., the 2022 rate-hike bear market) "
        "while staying invested during bull runs, yielding a much higher Sharpe ratio.", body))

    story.append(Paragraph("6.3 Results", h2))
    d5_data = [
        ["Strategy", "Ann. Return (%)", "Ann. Vol (%)", "Sharpe Ratio", "Max DD (%)"],
        ["Benchmark 1: SMA Portfolio",         "11.51", "18.97", "0.6064", "-37.71"],
        ["Benchmark 2: TopK Momentum (K=10)",  "27.79", "27.59", "1.0072", "-43.25"],
        ["New Strategy 1: RiskAdj Momentum",   "25.05", "21.92", "1.1431", "-39.69"],
        ["New Strategy 2: MarketTimed Momentum","24.70","18.23", "1.3547", "-11.84"],
    ]
    ts = TableStyle([
        ("BACKGROUND", (0,0), (-1,0), BLUE),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 9),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("ALIGN",      (0,1), (0,-1), "LEFT"),
        ("FONTNAME",   (0,1), (-1,1), "Helvetica"),
        ("FONTNAME",   (0,2), (-1,2), "Helvetica"),
        ("FONTNAME",   (0,3), (-1,3), "Helvetica-Bold"),
        ("FONTNAME",   (0,4), (-1,4), "Helvetica-Bold"),
        ("BACKGROUND", (0,3), (-1,4), colors.HexColor("#d4edda")),
        ("ROWBACKGROUNDS", (0,1), (-1,2), [colors.white, LIGHT_BLUE]),
        ("GRID",       (0,0), (-1,-1), 0.4, colors.HexColor("#aaaaaa")),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ])
    t5 = Table(d5_data, colWidths=[2.5*inch, 1.1*inch, 1.0*inch, 1.1*inch, 1.0*inch])
    t5.setStyle(ts)
    story.append(t5)
    story.append(Paragraph("Green rows = new strategies. Both exceed both benchmark Sharpe ratios.",
                            ParagraphStyle("caption", parent=base["Normal"], fontSize=8,
                                           textColor=colors.grey, spaceAfter=8)))

    story.append(Paragraph("6.4 Analysis", h2))
    story.append(Paragraph(
        "<b>New Strategy 1 (RiskAdj Momentum, Sharpe 1.143)</b> improves over TopK Momentum (1.007) "
        "primarily by reducing volatility from 27.59% to 21.92% through the RSI overbought filter "
        "and inverse-vol weighting. It avoids overextended names and concentrates capital in "
        "steady climbers.", body))
    story.append(Paragraph(
        "<b>New Strategy 2 (MarketTimed Momentum, Sharpe 1.355)</b> achieves the best overall "
        "performance across all strategies tested. Its maximum drawdown of only -11.84% is "
        "dramatically lower than all other strategies — nearly 4x better than the TopK benchmark "
        "(-43.25%). The 90-day equal-weighted market filter successfully identified the 2022 "
        "bear market and moved the portfolio to cash, avoiding the worst of the drawdown. "
        "Annualized return of 24.70% is only slightly below the TopK benchmark (27.79%), but "
        "with 34% lower volatility (18.23% vs 27.59%), the risk-adjusted return is far superior.", body))

    # ── Section 7 ────────────────────────────────────────────────────────────
    story.append(Paragraph("7. Conclusion", h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=MID_BLUE))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "This project delivers a complete, modular backtesting simulation system for "
        "Nasdaq-100 daily close strategies. Four key findings emerge:", body))
    conclusions = [
        ("<b>Momentum is the dominant signal.</b> All top-performing strategies use trailing "
         "return as their primary stock selection criterion. In the Nasdaq-100 over 2021–2026, "
         "momentum was consistently rewarded, particularly during the AI-driven bull market "
         "of 2023–2025."),
        ("<b>Risk management is as important as signal quality.</b> Strategies that combine "
         "momentum with risk controls (RSI filters, inverse-vol weighting, or market timing) "
         "achieve substantially better Sharpe ratios than pure momentum approaches."),
        ("<b>Market timing dramatically reduces drawdowns.</b> The 90-day broad-market filter "
         "in New Strategy 2 reduced maximum drawdown from -43% to -12% — nearly a 4x "
         "improvement — while preserving most of the upside return."),
        ("<b>Contrarian strategies underperform in trending markets.</b> Mean reversion, "
         "Bollinger Band, and RSI strategies all struggle in the sustained uptrend environment "
         "of this dataset."),
    ]
    for i, c in enumerate(conclusions, 1):
        story.append(Paragraph(f"{i}. {c}", bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "The system is fully extensible — adding a new strategy requires only implementing "
        "generate_weights() in a new file in the strategies/ directory, with no changes to "
        "the engine, metrics, or output modules.", body))

    doc.build(story)
    print(f"Saved: {OUTPUT}")

if __name__ == "__main__":
    build()
