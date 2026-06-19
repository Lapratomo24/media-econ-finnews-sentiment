import pandas as pd
import os

# Set up our file directions
input_file = "data/raw/analyst_ratings_processed.csv"
output_file = "data/filtered_tech_news.csv"

print("🔄 Step 1: Loading the heavy news archive... This takes a few seconds.")

# Read the dataset (we specify usecols to save RAM memory in your browser)
try:
    df = pd.read_csv(input_file, usecols=["title", "date", "stock"])
except Exception as e:
    print(f"❌ Error loading file. Make sure your file name matches exactly. Details: {e}")
    exit()

# List of target Big Tech tickers from your topic choice
target_tickers = ["AAPL", "MSFT", "NVDA", "GOOG", "AMZN", "META", "TSLA"]

print(f"🔍 Step 2: Extracting records for tech firms: {target_tickers}")

# Filter rows where the 'stock' column matches one of our target tickers
# Using .str.upper() ensures case differences don't break our match
df["stock"] = df["stock"].astype(str).str.upper().str.strip()
filtered_df = df[df["stock"].isin(target_tickers)].copy()

# Rename the columns to make things clear for Member 2's regression script
filtered_df = filtered_df.rename(columns={"title": "headline", "stock": "ticker"})

print(f"💾 Step 3: Saving the clean dataset...")
os.makedirs("data", exist_ok=True)
filtered_df.to_csv(output_file, index=False)

print(f"✅ Success! Isolated {len(filtered_df)} relevant tech headlines.")
print(filtered_df.head(10))