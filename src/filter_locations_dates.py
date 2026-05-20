import os
import gzip
import glob
import json
import pandas as pd
from multiprocessing import Pool
from datetime import timedelta
from tqdm import tqdm
from config import RAW_DATA_DIR, OUTPUT_DIR, INCIDENTS, BBOX_FILE

# Load bounding boxes
if not os.path.exists(BBOX_FILE):
    raise FileNotFoundError(f"Bounding box file {BBOX_FILE} not found. Run collect_bboxes.py first.")

with open(BBOX_FILE, 'r') as f:
    BBOXES = json.load(f)

# Precompute date ranges for each incident
# t-2 to t+2 days
INCIDENT_DATE_RANGES = {}
for city, date_str in INCIDENTS.items():
    incident_date = pd.to_datetime(date_str)
    start_date = incident_date - timedelta(days=2)
    end_date = incident_date + timedelta(days=2)
    INCIDENT_DATE_RANGES[city] = {
        "start": start_date,
        "end": end_date,
        "bbox": BBOXES.get(city)
    }

def process_file(file_path):
    """
    Reads a gzipped CSV of tweets and filters them by date and location.
    Assumes tab-separated values.
    """
    try:
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            df = pd.read_csv(f, sep='\t', on_bad_lines="skip", dtype=str)

        # Assuming the columns are named 'tweet_date', 'latitude', 'longitude'
        if 'tweet_date' not in df.columns or 'latitude' not in df.columns or 'longitude' not in df.columns:
            # Note: Change column names here if they differ in the dataset
            return pd.DataFrame()

        # Convert coordinates to float
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        
        # Convert created_at to datetime
        df['tweet_date'] = pd.to_datetime(df['tweet_date'], errors='coerce')
        
        # Drop rows with missing crucial data
        df = df.dropna(subset=['tweet_date', 'latitude', 'longitude', 'tweet_text'])

        matched_tweets = []

        # Check each incident condition
        for city, conditions in INCIDENT_DATE_RANGES.items():
            start_date = conditions['start']
            end_date = conditions['end']
            bbox = conditions['bbox']
            
            if not bbox:
                continue

            # Filter by date
            date_mask = (df['tweet_date'] >= start_date) & (df['tweet_date'] <= end_date)
            
            # Filter by location
            lat_mask = (df['latitude'] >= bbox['lat_min']) & (df['latitude'] <= bbox['lat_max'])
            lon_mask = (df['longitude'] >= bbox['lon_min']) & (df['longitude'] <= bbox['lon_max'])
            
            # Combine masks
            city_df = df[date_mask & lat_mask & lon_mask].copy()
            
            if not city_df.empty:
                city_df['matched_incident'] = city
                matched_tweets.append(city_df)

        if matched_tweets:
            return pd.concat(matched_tweets, ignore_index=True)
        else:
            return pd.DataFrame()

    except Exception as e:
        print(f"⚠️ Error in {os.path.basename(file_path)}: {e}")
        return pd.DataFrame()

def main():
    print("Starting location and date filtering...")
    # Find all gzipped CSV files in the raw data directory
    # We use recursive=True in case data is nested in year/month folders
    all_files = glob.glob(os.path.join(RAW_DATA_DIR, "**", "*.csv.gz"), recursive=True)
    
    if not all_files:
        print(f"No files found in {RAW_DATA_DIR}")
        return

    NUM_CORES = 20  # Adjust based on SLURM allocation
    print(f"Processing {len(all_files)} files using {NUM_CORES} cores...")

    with Pool(processes=NUM_CORES) as pool:
        results = list(tqdm(pool.imap_unordered(process_file, all_files), total=len(all_files)))

    # Filter out empty dataframes
    results = [df for df in results if not df.empty]
    
    if results:
        final_df = pd.concat(results, ignore_index=True)
        out_path = os.path.join(OUTPUT_DIR, "location_date_filtered_tweets.csv.gz")
        final_df.to_csv(out_path, index=False, compression="gzip", sep='\t')
        print(f"✅ Saved {len(final_df)} tweets to {out_path}")
    else:
        print("No tweets matched the criteria.")

if __name__ == "__main__":
    main()
