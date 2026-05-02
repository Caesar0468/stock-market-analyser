import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker: str, period: str, interval: str) -> pd.DataFrame:
    """Fetch OHLCV data for a single ticker from Yahoo Finance."""
    print(f"  Fetching {ticker}...")
    df = yf.download(ticker, period=period, interval=interval, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    if df.empty:
        raise ValueError(f"No data returned for ticker: {ticker}")

    df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.dropna(inplace=True)
    return df


def fetch_multiple(tickers: list, period: str, interval: str) -> dict:
    """Fetch data for multiple tickers. Returns {ticker: DataFrame}."""
    results = {}
    for ticker in tickers:
        try:
            results[ticker] = fetch_stock_data(ticker, period, interval)
        except Exception as e:
            print(f"  WARNING: Could not fetch {ticker}: {e}")
    return results