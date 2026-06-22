import pandas as pd

print("Loading datasets...")
# Read both files
sentiment_df = pd.read_csv("data/sentiment_scores.csv")
market_df = pd.read_csv("data/market_data.csv")

# Standardize date formats to strings so they line up cleanly
sentiment_df['date'] = pd.to_datetime(sentiment_df['date']).dt.strftime('%Y-%m-%d')
market_df['date'] = pd.to_datetime(market_df['date']).dt.strftime('%Y-%m-%d')

print("Averaging sentiment scores by day and ticker...")
# Average multiple headlines on the same day for a single stock
daily_sent = sentiment_df.groupby(['date', 'ticker'])['negative_sentiment'].mean().reset_index()

print("Merging news data with stock market values...")
# Combine the tables side-by-side using date and ticker as the keys
final_df = pd.merge(market_df, daily_sent, on=['date', 'ticker'], how='inner')

# Save the combined master file
final_df.to_csv("data/final_regression_data.csv", index=False)
print(f"Success! Master regression file created with {len(final_df)} rows.")