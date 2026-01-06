import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# ==========================================================
# Chargement des variables d'environnement (.env)
# ==========================================================
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# ==========================================================
# Connexion à PostgreSQL via SQLAlchemy
# ==========================================================
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ==========================================================
# Chemins du projet
# ==========================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SILVER_PATH = os.path.join(BASE_DIR, "data/silver/historical/co")

# ==========================================================
# Nom de la table cible
# ==========================================================
TABLE_NAME = "silver_co_measurements"

print("🚀 Début du chargement des données Silver CO vers PostgreSQL")

# ==========================================================
# Lecture et chargement de chaque fichier Silver
# ==========================================================
for file_name in sorted(os.listdir(SILVER_PATH)):
    if file_name.endswith("_CO_silver.csv"):
        file_path = os.path.join(SILVER_PATH, file_name)
        print(f"🔹 Chargement du fichier : {file_name}")

        # Lecture du CSV Silver
        df = pd.read_csv(file_path)

        # Conversion explicite de la colonne datetime
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

        # Insertion dans PostgreSQL
        df.to_sql(
            TABLE_NAME,
            engine,
            if_exists="append",  # on ajoute les données
            index=False,
            method="multi",  # insertion optimisée
        )

        print(f"✅ Données insérées depuis {file_name}")

print("🎉 Chargement terminé avec succès")
