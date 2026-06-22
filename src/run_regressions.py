import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

# 1. Load and clean the data
df = pd.read_csv("data/final_regression_data.csv")
df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna(subset=['return', 'volume', 'negative_sentiment'])

# 2. Run Model 1: Stock Returns
model1 = smf.ols("Q('return') ~ negative_sentiment", data=df).fit()
print("\n=== RETURNS MODEL SUMMARY ===")
print(model1.summary())

# 3. Run Model 2: Trading Volume
model2 = smf.ols("Q('volume') ~ negative_sentiment", data=df).fit()
print("\n=== VOLUME MODEL SUMMARY ===")
print(model2.summary())

# 4. Save both outputs automatically to the data folder
with open("data/model1_returns.txt", "w") as f:
    f.write(model1.summary().as_text())

with open("data/model2_volume.txt", "w") as f:
    f.write(model2.summary().as_text())

print("\nSuccess! Full regression summaries saved to the 'data/' folder.")