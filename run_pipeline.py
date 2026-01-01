"""
Initial Pipeline - Extract Only
Calls the extraction scripts you have already created:
- Historical CO
- Forecast Paris
- Real-Time Data
"""

import subprocess

print("🚀 Starting Extraction Pipeline...")

# 1️⃣ Extract Historical CO
print("\n[1] Extracting Historical CO Data...")
subprocess.run(["python", "src/extract/airparif_extract_historical_co.py"], check=True)

# 2️⃣ Extract Forecast Paris
print("\n[2] Extracting Forecast Data for Paris...")
subprocess.run(["python", "src/extract/airparif_extract_forecast_paris.py"], check=True)

# 3️⃣ Extract Real-Time Data
print("\n[3] Extracting Real-Time Air Quality Data for Paris...")
subprocess.run(["python", "src/extract/airparif_extract_realtime.py"], check=True)

print("\n🎉 Extraction Pipeline Completed Successfully!")
