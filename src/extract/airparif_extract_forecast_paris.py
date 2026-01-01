import os
import json
from datetime import datetime
import requests
from dotenv import load_dotenv

# 1 Carrega a chave do .env
load_dotenv()
API_KEY = os.getenv("AIRPARIF_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Please set AIRPARIF_API_KEY in .env file.")

# 2 Endpoint da API (índices de qualidade do ar por município)
URL = "https://api.airparif.fr/indices/prevision/commune"

# 3 Parâmetros da query
# 75104 é o código INSEE para Paris
params = {"insee": "75104"}

# 4 Header com a chave de API
headers = {"X-Api-Key": API_KEY}

# 5 Requisição GET
response = requests.get(URL, headers=headers, params=params)
response.raise_for_status()  # Vai gerar erro se status != 200
data = response.json()

# 6 Cria diretório para dados brutos, se não existir
RAW_DATA_PATH = "data/raw/forecast"
os.makedirs(RAW_DATA_PATH, exist_ok=True)

# 7 Salva arquivo JSON com timestamp
ingestion_date = datetime.utcnow().strftime("%Y-%m-%d")
file_name = f"airparif_raw_{ingestion_date}.json"
file_path = os.path.join(RAW_DATA_PATH, file_name)

with open(file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print(f"✅ Raw data successfully saved at {file_path}")
