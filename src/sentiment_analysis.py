import pandas as pd
import os

input_file = "data/filtered_tech_news.csv"
output_file = "data/sentiment_scores.csv"

print("🔄 Loading your filtered tech headlines...")
df = pd.read_csv(input_file)

# A vetted, strong baseline list of negative financial keywords
# (Derived from the academic Loughran-McDonald finance dictionary standard)
negative_words = {
    'loss', 'losses', 'drop', 'drops', 'dropped', 'dropping', 'decline', 'declines', 'declining', 
    'fall', 'falls', 'fell', 'falling', 'plummet', 'plummets', 'crash', 'crashed', 'crashing', 
    'lawsuit', 'sue', 'sued', 'suing', 'litigation', 'investigation', 'probe', 'probes', 'fined', 
    'fine', 'deficit', 'bankruptcy', 'fail', 'fails', 'failed', 'failing', 'failure', 'shrink', 
    'shrank', 'slump', 'slumps', 'slumped', 'warn', 'warns', 'warned', 'warning', 'bad', 'worst', 
    'miss', 'misses', 'missed', 'missing', 'disappoint', 'disappoints', 'disappointed', 'weak'
}

print("🧠 Analyzing text sentiment counts...")

def calculate_negative_score(headline):
    if not isinstance(headline, str):
        return 0.0
    # Clean up the text: make it lowercase and split into individual words
    words = headline.lower().split()
    if len(words) == 0:
        return 0.0
    
    # Count how many words match our negative financial word list
    neg_count = sum(1 for word in words if word.strip(".,!?;:()\"'") in negative_words)
    
    # Return the proportion of negative words to total words
    return float(neg_count / len(words))

# Apply the function across every headline row
df["negative_sentiment"] = df["headline"].apply(calculate_negative_score)

# Keep only the essential columns Member 2 needs for the regressions
final_df = df[["date", "ticker", "negative_sentiment"]].copy()

# Ensure the Date column is stripped down to just YYYY-MM-DD for clean data merging later
final_df["date"] = pd.to_datetime(final_df["date"], utc=True).dt.date

print("💾 Saving the final sentiment arrays...")
final_df.to_csv(output_file, index=False)

print(f"✅ Success! Generated sentiment metrics and saved to '{output_file}'")
print(final_df.head(10))