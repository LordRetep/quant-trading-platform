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
    
    # Handle multi-level columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)  # Use first level of column names
    
    # Rename columns to match Backtrader's expected format
    df = df.rename(columns={
        'Open': 'open', 'High': 'high', 'Low': 'low',
        'Close': 'close', 'Volume': 'volume', 'Adj Close': 'adj_close'
    })
    
    # Select only required columns
    required_columns = ['open', 'high', 'low', 'close', 'volume']
    available_columns = [col for col in required_columns if col in df.columns]
    if not available_columns:
        raise ValueError(f"Data for {asset} missing required columns: {required_columns}")
    
    df = df[available_columns]
    df.dropna(inplace=True)
    
    # Ensure index is datetime
    df.index = pd.to_datetime(df.index)
    
    return df