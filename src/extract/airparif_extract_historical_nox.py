import os
import requests


ITEMS = {
    2023: "993a489447504386b39ff9afaf91ed5d",
    2024: "4408ee1f75ca4b5c88d1b1949e4bc78c",
    2025: "9599dabcc1ad45e1bd35061587636964",
}

RAW_PATH = "data/raw/historical/nox"
os.makedirs(RAW_PATH, exist_ok=True)

for year, item_id in ITEMS.items():
    url = f"https://www.arcgis.com/sharing/rest/content/items/{item_id}/data"
    # https://www.arcgis.com/sharing/rest/content/items/993a489447504386b39ff9afaf91ed5d/data

    output_file = os.path.join(RAW_PATH, f"{year}_NOX.csv")

    response = requests.get(url)
    response.raise_for_status()

    with open(output_file, "wb") as file:
        file.write(response.content)

    print(f"Downloaded NOx data for {year} to {output_file}")
