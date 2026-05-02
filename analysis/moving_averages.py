import pandas as pd


def add_moving_averages(df: pd.DataFrame, short: int = 20, long: int = 50) -> pd.DataFrame:
    df = df.copy()
    # Flatten multi-level columns if present (newer yfinance versions)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df[f"MA{short}"] = df["Close"].rolling(window=short).mean()
    df[f"MA{long}"] = df["Close"].rolling(window=long).mean()
    return df


def summary_stats(df: pd.DataFrame) -> dict:
    close = df["Close"].squeeze()  # flatten Series-of-Series if needed
    return {
        "last_price":  round(float(close.iloc[-1]), 2),
        "period_high": round(float(close.max()), 2),
        "period_low":  round(float(close.min()), 2),
        "pct_change":  round(float((close.iloc[-1] - close.iloc[0]) / close.iloc[0] * 100), 2),
    }