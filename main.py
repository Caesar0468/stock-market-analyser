import config
from data.fetcher import fetch_multiple
from analysis.moving_averages import add_moving_averages, summary_stats
from analysis.signals import generate_signals, latest_signals
from visualization.plotter import plot_stock


def analyze(ticker: str, df) -> None:
    print(f"\n{'='*50}")
    print(f"  {ticker}")
    print(f"{'='*50}")

    short_col = f"MA{config.MA_SHORT}"
    long_col  = f"MA{config.MA_LONG}"

    df = add_moving_averages(df, config.MA_SHORT, config.MA_LONG)
    df = generate_signals(df, short_col, long_col)

    stats = summary_stats(df)
    print(f"  Last price : ${stats['last_price']}")
    print(f"  Period high: ${stats['period_high']}")
    print(f"  Period low : ${stats['period_low']}")
    print(f"  Change     : {stats['pct_change']:+.2f}%")

    sigs = latest_signals(df)
    if sigs.empty:
        print("  Signals    : none in period")
    else:
        print("  Latest signals:")
        for date, row in sigs.iterrows():
            tag = "▲ BUY " if row["Signal"] == "BUY" else "▼ SELL"
            print(f"    {tag}  {date.date()}  ${row['Close']:.2f}")

    plot_stock(ticker, df, short_col, long_col, config.REPORT_DIR)


def main():
    print("Stock Market Analyzer")
    print(f"Fetching {len(config.TICKERS)} tickers — period={config.PERIOD}\n")

    stocks = fetch_multiple(config.TICKERS, config.PERIOD, config.INTERVAL)

    for ticker, df in stocks.items():
        analyze(ticker, df)

    print(f"\nDone. Charts saved to /{config.REPORT_DIR}/")


if __name__ == "__main__":
    main()