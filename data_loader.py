import yfinance as yf

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
    df.dropna(inplace=True)
    return df
