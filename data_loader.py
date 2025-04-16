import yfinance as yf
import pandas as pd
from datetime import datetime, date
import time
import os

SYMBOL_MAP = {
    "GBPUSD": "GBPUSD=X",
    "EURUSD": "EURUSD=X",
    "EURGBP": "EURGBP=X",
    "USDJPY": "USDJPY=X",
    "EURCHF": "EURCHF=X",
    "OIL": "CL=F",
    "GOLD": "GC=F",
    "SILVER": "SI=F"
}

# Sample CSV data for fallback (replace with actual data)
SAMPLE_DATA = {
    "GBPUSD": pd.DataFrame({
        "open": [1.36, 1.37, 1.35], "high": [1.37, 1.38, 1.36],
        "low": [1.35, 1.36, 1.34], "close": [1.36, 1.37, 1.35],
        "volume": [1000, 1100, 1200]
    }, index=pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"])),
    "EURUSD": pd.DataFrame({
        "open": [1.07, 1.08, 1.06], "high": [1.08, 1.09, 1.07],
        "low": [1.06, 1.07, 1.05], "close": [1.07, 1.08, 1.06],
        "volume": [1000, 1100, 1200]
    }, index=pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"])),
    "GOLD": pd.DataFrame({
        "open": [1800, 1810, 1790], "high": [1810, 1820, 1800],
        "low": [1790, 1800, 1780], "close": [1800, 1810, 1790],
        "volume": [1000, 1100, 1200]
    }, index=pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"])),
    "SILVER": pd.DataFrame({
        "open": [24.0, 24.5, 23.5], "high": [24.5, 25.0, 24.0],
        "low": [23.5, 24.0, 23.0], "close": [24.0, 24.5, 23.5],
        "volume": [1000, 1100, 1200]
    }, index=pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]))
}

def get_data(asset, start, end, max_retries=3):
    ticker = SYMBOL_MAP[asset]
    try:
        # Ensure dates are valid and not in the future
        today = date.today()
        start = pd.to_datetime(start)
        end = min(pd.to_datetime(end), pd.to_datetime(today))
        start_str = start.strftime('%Y-%m-%d')
        end_str = end.strftime('%Y-%m-%d')

        # Try yfinance with retries
        for attempt in range(max_retries):
            try:
                df = yf.download(ticker, start=start_str, end=end_str, progress=False)
                if not df.empty:
                    break
                print(f"Warning: No data for {asset} ({ticker}) from {start_str} to {end_str}, attempt {attempt + 1}/{max_retries}")
                time.sleep(1)
            except Exception as e:
                print(f"Warning: Attempt {attempt + 1} failed for {asset} ({ticker}): {str(e)}")
                time.sleep(1)
        else:
            # Fallback to sample data or CSV
            print(f"Warning: yfinance failed for {asset} ({ticker}), using fallback data")
            if asset in SAMPLE_DATA:
                df = SAMPLE_DATA[asset]
                # Filter by date range
                df = df[(df.index >= start) & (df.index <= end)]
                if df.empty:
                    print(f"Warning: Fallback data empty for {asset} in range {start_str} to {end_str}")
                    return df
            else:
                print(f"Warning: No fallback data for {asset}")
                return pd.DataFrame()

        # Handle multi-level columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        # Rename columns to match Backtrader's expected format
        df = df.rename(columns={
            'Open': 'open', 'High': 'high', 'Low': 'low',
            'Close': 'close', 'Volume': 'volume', 'Adj Close': 'adj_close'
        })
        
        # Select only required columns
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        available_columns = [col for col in required_columns if col in df.columns]
        if not available_columns:
            print(f"Warning: Data for {asset} missing required columns: {required_columns}")
            return pd.DataFrame()
        
        df = df[available_columns]
        df.dropna(inplace=True)
        
        # Ensure index is datetime
        df.index = pd.to_datetime(df.index)
        
        return df
    except Exception as e:
        print(f"Warning: Failed to retrieve data for {asset} ({ticker}): {str(e)}")
        return pd.DataFrame()