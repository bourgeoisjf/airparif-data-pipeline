import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# 1️⃣ Carrega a chave da API do arquivo .env
load_dotenv()
API_KEY = os.getenv("AIRPARIF_API_KEY")

# 2️⃣ Endpoint API – previsão para Paris (INSEE 75104)
URL = "https://api.airparif.fr/indices/prevision/commune"

# 3️⃣ Parâmetros da requisição
params = {
    "insee": "75104"  # Paris
}

# 4️⃣ Headers com a chave da API
headers = {"X-Api-Key": API_KEY}

# 5️⃣ Faz a requisição
response = requests.get(URL, headers=headers, params=params)
response.raise_for_status()
data = response.json()

# 6️⃣ Cria diretório raw/realtime/paris
RAW_PATH = "data/raw/realtime/paris"
os.makedirs(RAW_PATH, exist_ok=True)

# 7️⃣ Salva JSON bruto com timestamp
ingestion_date = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"airparif_realtime_paris_{ingestion_date}.json"
file_path = os.path.join(RAW_PATH, file_name)

with open(file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print(f"✅ Real-time air quality data saved at {file_path}")
