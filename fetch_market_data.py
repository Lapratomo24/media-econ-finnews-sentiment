import pandas as pd
import yfinance as yf

tickers = ["AAPL", "MSFT", "NVDA", "GOOG", "AMZN", "FB", "TSLA"]
all_data = []

print("Downloading historical stock data (2009 - 2020)...")

for ticker in tickers:
    print(f"Fetching {ticker}...")
    # Pull data
    data = yf.download(ticker, start="2009-01-01", end="2020-07-01", progress=False)
    
    if not data.empty:
        # Reset date index to turn it into a regular column
        data = data.reset_index()
        
        # Create an empty DataFrame for this specific ticker
        ticker_df = pd.DataFrame()
        
        # Look through the columns and unpack the MultiIndex tuples
        for col in data.columns:
            # Check if it's a tuple (e.g., ('Close', 'AAPL') or ('Date', ''))
            metric = col[0] if isinstance(col, tuple) else col
            metric_lower = str(metric).lower().strip()
            
            if 'date' in metric_lower:
                ticker_df['date'] = data[col]
            elif 'close' in metric_lower:  # This will catch 'Close' or 'Adj Close'
                ticker_df['adj_close'] = data[col]
            elif 'volume' in metric_lower:
                ticker_df['volume'] = data[col]
        
        # Add the ticker identity column
        ticker_df['ticker'] = ticker
        all_data.append(ticker_df)

# Combine all DataFrames together
df = pd.concat(all_data, ignore_index=True)

# Rebrand 'FB' to 'META' to match your text sentiment file perfectly
df['ticker'] = df['ticker'].replace({'FB': 'META'})

# Standardize date formats to text strings
df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

# Calculate daily percentage returns properly per stock group
df['return'] = df.groupby('ticker')['adj_close'].pct_change()

# Save the clean output
df.to_csv("data/market_data.csv", index=False)
print("Saved clean historical market data to data/market_data.csv!")