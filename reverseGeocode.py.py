import pandas as pd
import numpy as np
import requests
import json
import os
import time
from collections import deque
import sys

input_file = "C:/HRI DATA/Downloads/test_coordinates.csv"
output_file = "C:/HRI DATA/Downloads/output.csv"
api_key = 'JI0AUlZPpeJLaDuMJtUIESD4LeKyCAUnObU8R3Gy'
retries = 3
rolling_window = 10
save_every = 100

# to be extracted
address_components = ["country", "administrative_area_level_1", "administrative_area_level_2", "administrative_area_level_3", "postal_code"]

# load input file
input_df = pd.read_csv(input_file)

# check missing columns
for component in address_components + ["formatted_address"]:
    if component not in input_df.columns:
        input_df[component] = None

# logic

if os.path.exists(output_file):
    existing_df = pd.read_csv(output_file)
    input_df.update(existing_df)
    if "formatted_address" in existing_df.columns:
        filled_rows = existing_df['formatted_address'].notna()
        starting_index = filled_rows.sum()
    else:
        starting_index = 0
    print('starting from current index')
else:
    print('starting from beginning')
    starting_index = 0

session = requests.Session()

def get_address_components(lat, lon, retries):
    url = "https://api.olamaps.io/places/v1/reverse-geocode?latlng=12.923946516889448,77.5526110768168&api_key=JI0AUlZPpeJLaDuMJtUIESD4LeKyCAUnObU8R3Gy"
    for attempt in range(retries):
        try:
            response = session.get(url,timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])

                if not results:
                    continue

                result = results[0]
                components = result.get("address_components", [])
                extracted = {}

                for comp in components:
                    types = comp['types']
                    if "country" in types:
                        extracted["country"] = comp["long_name"]
                    elif "administrative_area_level_1" in types:
                        extracted["administrative_area_level_1"] = comp["long_name"]
                    elif "administrative_area_level_2" in types:
                        extracted["administrative_area_level_2"] = comp["long_name"]
                    elif "administrative_area_level_3" in types:
                        extracted["administrative_area_level_3"] = comp["long_name"]
                    elif "postal_code" in types:
                        extracted["postal_code"] = comp["long_name"]

                extracted["formatted_address"] = result.get("formatted_address", None)
                return extracted

        except Exception as e:
            if attempt == retries - 1:
                print(f"\nFailed for lat={lat}, lon={lon} after {retries} attempts: {e}")

    return None

# will give status of the process loop

start_time = time.time()
durations = deque(maxlen=rolling_window)
total = len(input_df)

for idx in range(starting_index, total):
    row = input_df.iloc[idx]
    lat, lon = row["Latitude"], row["Longitude"]

    iter_start = time.time()
    result = get_address_components(lat, lon, retries)

    if result:
        for key,value in result.items():
            input_df.at[idx, key] = value
    else:
        print(f"\nNo result for index {idx} (lat={lat}, lon={lon}) after retries")

    if idx % save_every == 0 or idx == total-1:
        input_df.to_csv(output_file, index=False)

    iter_duration = time.time() - start_time
    durations.append(iter_duration)
    completed = idx+1

    avg_time = sum(durations) / len(durations) if durations else 1
    remaining = total - completed
    eta_left = remaining * avg_time

    elapsed = time.time() - start_time
    eta_mins, eta_secs = divmod(eta_left, 60)
    elapsed_mins, elapsed_secs = divmod(elapsed, 60)

    percent = (completed/total) * 100
    sys.stdout.write(f"\rProcessing row {idx + 1}/{total} | {percent:.2f}% complete | ETA: {int(eta_mins)}m {int(eta_secs)}s | Elapsed: {int(elapsed_mins)}m {int(elapsed_secs)}s")
    sys.stdout.flush()

# Column rename
input_df.rename(columns={
    "country": "Country",
    "administrative_area_level_1": "State",
    "administrative_area_level_2": "City",
    "administrative_area_level_3": "Region"
}, inplace=True)

# Final save to output file
input_df.to_csv(output_file, index=False)
print(f"\nAll coordinates are processed and saved to CSV.")

