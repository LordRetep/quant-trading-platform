import yfinance as yf
import pandas as pd
from datetime import datetime

SYMBOL_MAP = {
    "GBPUSD": "GBPUSD=X",
    "EURUSD": "EURUSD=X",
    "EURGBP": "EURGBP=X",
    "USDJPY": "JPY=X",
    "EURCHF": "EURCHF=X",
    "OIL": "CL=F",
    "GOLD": "GC=F",
    "SILVER": "SI=F"
}

def get_data(asset, start, end):
    ticker = SYMBOL_MAP[asset]
    try:
        # Ensure dates are in correct format
        start = pd.to_datetime(start).strftime('%Y-%m-%d')
        end = pd.to_datetime(end).strftime('%Y-%m-%d')
        
        # Download data
        df = yf.download(ticker, start=start, end=end, progress=False)
        
        if df.empty:
            print(f"Warning: No data retrieved for {asset} ({ticker}) from {start} to {end}")
            return df
        
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