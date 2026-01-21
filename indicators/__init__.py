import pandas as pd
from data.data_loader import load_price_data


def compute_sma(df: pd.DataFrame, window: int, price_col: str = "Close") -> pd.Series:
    """
    Simple moving average
    """
    return df[price_col].rolling(window=window).mean()


def compute_rsi(df: pd.DataFrame, period: int = 14, price_col: str = "Close") -> pd.Series:
    """
    RSI
    """
    delta = df[price_col].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def compute_atr(df: pd.DataFrame, period: int = 14) -> tuple[pd.Series, pd.Series]:
    """
    (ATR) and ATR%
    """
    high = df["High"]
    low = df["Low"]
    close = df["Close"]
    prev_close = close.shift(1)

    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(period).mean()
    atr_pct = (atr / close) * 100

    return atr, atr_pct


def add_indicators(
    df: pd.DataFrame,
    short_window: int = 35,
    long_window: int = 100,
    rsi_period: int = 14,
    atr_period: int = 14,
) -> pd.DataFrame:
    """
    Adding SMA, RSI and ATR indicators
    """
    df = df.copy()

    df[f"SMA_{short_window}"] = compute_sma(df, short_window)
    df[f"SMA_{long_window}"] = compute_sma(df, long_window)

    df["RSI"] = compute_rsi(df, rsi_period)

    atr, atr_pct = compute_atr(df, atr_period)
    df["ATR"] = atr
    df["ATR_pct"] = atr_pct

    return df


if __name__ == "__main__":
    # Basic test
    df_gold = load_price_data("GC=F", start="2010-01-01")
    df_gold_ind = add_indicators(df_gold)

    print(df_gold_ind.tail()[[
        "Close",
        "SMA_35",
        "SMA_100",
        "RSI",
        "ATR",
        "ATR_pct",
    ]])
