import os
import pandas as pd
from tqdm import tqdm
from config import OUTPUT_DIR, REGEX_PATTERN

def filter_by_keywords():
    input_file = os.path.join(OUTPUT_DIR, "location_date_filtered_tweets.csv.gz")
    output_file = os.path.join(OUTPUT_DIR, "final_filtered_tweets.csv.gz")

    if not os.path.exists(input_file):
        print(f"Input file {input_file} not found. Please run filter_locations_dates.py first.")
        return

    print(f"Loading {input_file}...")
    df = pd.read_csv(input_file, compression='gzip', sep='\t', dtype=str)
    
    if 'tweet_text' not in df.columns:
        print("Error: 'tweet_text' column not found in dataset.")
        return

    print(f"Total tweets before keyword filtering: {len(df)}")
    
    # Drop NAs in text
    df = df.dropna(subset=['tweet_text'])
    
    # We use vectorised string matching
    # match exact keywords using regex pattern compiled in config.py
    tqdm.pandas(desc="Filtering Keywords")
    
    # Find matching tweets
    mask = df['tweet_text'].str.contains(REGEX_PATTERN, na=False, regex=True)
    
    final_df = df[mask].copy()
    
    print(f"Total tweets after keyword filtering: {len(final_df)}")
    
    final_df.to_csv(output_file, index=False, compression='gzip', sep='\t')
    print(f"✅ Saved final filtered dataset to {output_file}")

if __name__ == "__main__":
    filter_by_keywords()
