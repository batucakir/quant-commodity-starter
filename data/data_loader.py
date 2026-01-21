import subprocess
import sys

def install_if_missing(package):
    try:
        __import__(package)
        print(f"[OK] {package} already installed")
    except ImportError:
        print(f"[INFO] Installing missing package: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_if_missing("yfinance")
install_if_missing("pandas")



import yfinance as yf
import pandas as pd

COMMODITY_SYMBOLS = {
    "gold_futures": "GC=F",
    "silver_futures": "SI=F",
    "copper": "HG=F",
    "platinum": "PL=F",
    "palladium": "PA=F"
}

def load_price_data(symbol, start="2005-01-01"):
    """
    Download historical daily price data
    """
    df = yf.download(symbol, start=start)
    
    if df.empty:
        print(f"[WARN] No data downloaded for {symbol}. Returning empty DataFrame.")
        return df
    
    df = df[["Open", "High", "Low", "Close", "Volume"]]
    df.dropna(inplace=True)
    return df

def load_all_commodities(start="2005-01-01"):
    """
    Load all predefined commodities
    """
    data = {}
    for name, symbol in COMMODITY_SYMBOLS.items():
        df = load_price_data(symbol, start)
        df["commodity"] = name
        data[name] = df
    return data

if __name__ == "__main__":
    all_data = load_all_commodities()

    for commodity, df in all_data.items():
        print(f"\n{commodity.upper()}")
        print(df.tail())
