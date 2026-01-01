import os
import pandas as pd
import json
import os

# Project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Paths
RAW_PATH = os.path.join(BASE_DIR, "data/raw/historical/co")
SILVER_PATH = os.path.join(BASE_DIR, "data/silver/historical/co")
os.makedirs(SILVER_PATH, exist_ok=True)


# Metadata dictionary
metadata_dict = {}

# Process each year CSV
for file_name in os.listdir(RAW_PATH):
    if file_name.endswith(".csv"):
        year = file_name.split("_")[0]
        raw_file = os.path.join(RAW_PATH, file_name)
        print(f"🔹 Processing {raw_file}...")

        # Read raw CSV, skip metadata lines later
        with open(raw_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Extract metadata
        station_codes = lines[2].strip().split(",")[1:]
        station_names = lines[1].strip().split(",")[1:]
        substances = lines[4].strip().split(",")[1:]
        units = lines[5].strip().split(",")[1:]

        # Build column names for Silver
        silver_columns = [
            f"{code}_{substance}" for code, substance in zip(station_codes, substances)
        ]
        metadata_dict[year] = {
            col: {
                "station_code": code,
                "station_name": name,
                "substance": sub,
                "unit": unit,
            }
            for col, code, name, sub, unit in zip(
                silver_columns, station_codes, station_names, substances, units
            )
        }

        # Read actual data (skip first 6 lines)
        data = pd.read_csv(raw_file, skiprows=6)

        # Rename columns
        rename_dict = {
            data.columns[i + 1]: silver_columns[i] for i in range(len(silver_columns))
        }
        data.rename(columns=rename_dict, inplace=True)

        # Convert datetime
        data[data.columns[0]] = pd.to_datetime(data[data.columns[0]], errors="coerce")
        data.rename(columns={data.columns[0]: "datetime"}, inplace=True)

        # Convert measurement columns to float
        for col in silver_columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

        # Save cleaned Silver CSV
        silver_file = os.path.join(SILVER_PATH, f"{year}_CO_silver.csv")
        data.to_csv(silver_file, index=False)
        print(f"✅ Saved Silver CSV: {silver_file}")

# Save metadata to JSON
metadata_file = os.path.join(SILVER_PATH, "CO_metadata.json")
with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(metadata_dict, f, ensure_ascii=False, indent=2)
print(f"✅ Saved metadata JSON: {metadata_file}")
