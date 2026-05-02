import pandas as pd


def generate_signals(df: pd.DataFrame, short_col: str, long_col: str) -> pd.DataFrame:
    """
    Golden cross  → BUY  (short MA crosses above long MA)
    Death cross   → SELL (short MA crosses below long MA)
    Returns a copy of df with a 'Signal' column: 'BUY', 'SELL', or None.
    """
    df = df.copy()
    df["Signal"] = None

    above = df[short_col] > df[long_col]
    crossover = above & ~above.shift(1).fillna(False)   # just turned True
    crossunder = ~above & above.shift(1).fillna(False)  # just turned False

    df.loc[crossover, "Signal"] = "BUY"
    df.loc[crossunder, "Signal"] = "SELL"

    return df


def latest_signals(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Return the n most recent non-null signals."""
    return df[df["Signal"].notna()].tail(n)[["Close", "Signal"]]