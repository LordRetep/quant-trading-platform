import yfinance as yf
import pandas as pd

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
    df = yf.download(ticker, start=start, end=end)
    if df.empty:
        raise ValueError(f"No data retrieved for {asset} from {start} to {end}")
    
    # Rename columns to match Backtrader's expected format
    df = df.rename(columns={
        'Open': 'open', 'High': 'high', 'Low': 'low',
        'Close': 'close', 'Volume': 'volume'
    })
    
    # Ensure required columns exist
    required_columns = ['open', 'high', 'low', 'close', 'volume']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Data for {asset} missing required columns: {required_columns}")
    
    df.dropna(inplace=True)
    return df