import os
import requests

# 🔑 ITEM IDs reais (exemplo: 2023)
ITEMS = {
    2023: "d0eca32a84374a1e9a3fe1978a6fc345",
    2024: "f11063a559eb48ab9d15644091b72565",
    2025: "37efd2eeb29047e1bded9943bf96d021",
}

RAW_PATH = "data/raw/historical/co"
os.makedirs(RAW_PATH, exist_ok=True)

for year, item_id in ITEMS.items():
    print(f"⬇️ Downloading CO historical data for {year}...")

    url = f"https://www.arcgis.com/sharing/rest/content/items/{item_id}/data"

    output_file = os.path.join(RAW_PATH, f"{year}_CO.csv")

    response = requests.get(url)
    response.raise_for_status()

    # 🔴 salvar diretamente como CSV
    with open(output_file, "wb") as f:
        f.write(response.content)

    print(f"✅ Saved CO historical data: {output_file}")

print("🎉 Historical CO extraction completed successfully.")
