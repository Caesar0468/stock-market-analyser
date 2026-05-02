import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


def plot_stock(
    ticker: str,
    df: pd.DataFrame,
    short_col: str,
    long_col: str,
    output_dir: str = "reports",
) -> str:
    """
    Plot price + MAs + buy/sell signals + volume.
    Saves to output_dir/{ticker}.png and returns the path.
    """
    os.makedirs(output_dir, exist_ok=True)

    fig, (ax_price, ax_vol) = plt.subplots(
        2, 1, figsize=(14, 8),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True,
    )
    fig.patch.set_facecolor("#0d1117")
    for ax in (ax_price, ax_vol):
        ax.set_facecolor("#0d1117")
        ax.tick_params(colors="#8b949e", labelsize=9)
        for spine in ax.spines.values():
            spine.set_edgecolor("#21262d")

    dates = df.index

    # — Price line
    ax_price.plot(dates, df["Close"], color="#4a90d9", linewidth=1.8, label="Price", zorder=3)

    # — Moving averages
    if short_col in df.columns:
        ax_price.plot(dates, df[short_col], color="#f5a623", linewidth=1.2,
                      linestyle="--", label=short_col, zorder=2)
    if long_col in df.columns:
        ax_price.plot(dates, df[long_col], color="#9b59b6", linewidth=1.2,
                      linestyle="--", label=long_col, zorder=2)

    # — Buy / sell signals
    buys  = df[df["Signal"] == "BUY"]
    sells = df[df["Signal"] == "SELL"]
    ax_price.scatter(buys.index,  buys["Close"],  marker="^", color="#2d9b5c",
                     s=90, zorder=5, label="Buy signal")
    ax_price.scatter(sells.index, sells["Close"], marker="v", color="#d94f4f",
                     s=90, zorder=5, label="Sell signal")

    # — Volume bars (green/red by price direction)
    vol_colors = [
        "#2d9b5c" if df["Close"].iloc[i] >= df["Open"].iloc[i] else "#d94f4f"
        for i in range(len(df))
    ]
    ax_vol.bar(dates, df["Volume"], color=vol_colors, width=0.8, alpha=0.7)
    ax_vol.set_ylabel("Volume", color="#8b949e", fontsize=9)
    ax_vol.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"{x/1e6:.0f}M")
    )

    # — Labels & formatting
    ax_price.set_title(f"{ticker} — Price & Moving Averages", color="#e6edf3",
                       fontsize=14, fontweight="bold", pad=12)
    ax_price.set_ylabel("Price (USD)", color="#8b949e", fontsize=9)
    ax_price.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax_price.legend(loc="upper left", facecolor="#161b22", edgecolor="#21262d",
                    labelcolor="#e6edf3", fontsize=9)
    ax_price.grid(color="#21262d", linewidth=0.5, linestyle="-")
    ax_vol.grid(color="#21262d", linewidth=0.5, linestyle="-", axis="y")

    ax_vol.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    ax_vol.xaxis.set_major_locator(mdates.MonthLocator())
    plt.setp(ax_vol.xaxis.get_majorticklabels(), rotation=30, ha="right")

    plt.tight_layout()
    out_path = os.path.join(output_dir, f"{ticker}.png")
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"  Saved → {out_path}")
    return out_path