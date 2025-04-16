import yfinance as yf
import pandas as pd
from datetime import datetime, date

SYMBOL_MAP = {
    "GBPUSD": "GBPUSD=X",
    "EURUSD": "EURUSD=X",
    "EURGBP": "EURGBP=X",
    "USDJPY": "USDJPY=X",  # Updated ticker for consistency
    "EURCHF": "EURCHF=X",
    "OIL": "CL=F",
    "GOLD": "GC=F",
    "SILVER": "SI=F"
}

def get_data(asset, start, end):
    ticker = SYMBOL_MAP[asset]
    try:
        # Ensure dates are valid and not in the future
        today = date.today()
        start = pd.to_datetime(start)
        end = min(pd.to_datetime(end), pd.to_datetime(today))
        start_str = start.strftime('%Y-%m-%d')
        end_str = end.strftime('%Y-%m-%d')

        # Try primary date range
        df = yf.download(ticker, start=start_str, end=end_str, progress=False)
        
        if df.empty:
            print(f"Warning: No data for {asset} ({ticker}) from {start_str} to {end_str}")
            # Fallback: Try a shorter, recent range
            fallback_start = pd.to_datetime(today) - pd.Timedelta(days=365)
            df = yf.download(ticker, start=fallback_start, end=end_str, progress=False)
            if df.empty:
                print(f"Warning: Fallback range also empty for {asset} ({ticker})")
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