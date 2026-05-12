import yfinance as yf

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
    long_col = f"MA{config.MA_LONG}"

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

    plot_stock(
        ticker,
        df,
        short_col,
        long_col,
        config.REPORT_DIR
    )


def main():
    print("\nStock Market Analyzer")
    print("-" * 50)

    user_input = input(
        "Enter company names separated by commas:\n> "
    )

    company_names = [
        name.strip()
        for name in user_input.split(",")
        if name.strip()
    ]

    if not company_names:
        print("No company names entered.")
        return

    tickers = []

    print("\nFinding stock tickers...\n")

    for company in company_names:
        try:
            search = yf.Search(company, max_results=1)

            if not search.quotes:
                print(f"No ticker found for {company}")
                continue

            ticker = search.quotes[0]["symbol"]

            print(f"{company} → {ticker}")

            tickers.append(ticker)

        except Exception as e:
            print(f"Could not find {company}: {e}")

    if not tickers:
        print("\nNo valid tickers found.")
        return

    print(f"\nFetching {len(tickers)} stock(s)...\n")

    stocks = fetch_multiple(
        tickers,
        config.PERIOD,
        config.INTERVAL
    )

    for ticker, df in stocks.items():
        analyze(ticker, df)

    print(f"\nDone. Charts saved to /{config.REPORT_DIR}/")


if __name__ == "__main__":
    main()
