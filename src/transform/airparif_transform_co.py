import os
import pandas as pd
import json

# 📌 Répertoire racine du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 📂 Chemins des données
CHEMIN_BRONZE = os.path.join(BASE_DIR, "data/raw/historical/co")
CHEMIN_SILVER = os.path.join(BASE_DIR, "data/silver/historical/co")
os.makedirs(CHEMIN_SILVER, exist_ok=True)

# 📘 Dictionnaire pour stocker les métadonnées
metadonnees = {}

# 🔁 Traitement de chaque fichier CSV (un par année)
for nom_fichier in os.listdir(CHEMIN_BRONZE):
    if nom_fichier.endswith(".csv"):
        annee = nom_fichier.split("_")[0]
        fichier_brut = os.path.join(CHEMIN_BRONZE, nom_fichier)

        print(f"🔹 Traitement du fichier : {fichier_brut}")

        # 📖 Lecture du fichier brut ligne par ligne (pour extraire les métadonnées)
        with open(fichier_brut, "r", encoding="utf-8") as f:
            lignes = f.readlines()

        # 🧾 Extraction des métadonnées depuis les lignes d’en-tête
        codes_stations = lignes[2].strip().split(",")[1:]
        noms_stations = lignes[1].strip().split(",")[1:]
        substances = lignes[4].strip().split(",")[1:]
        unites = lignes[5].strip().split(",")[1:]

        # 🏷️ Construction des noms de colonnes pour la couche Silver
        colonnes_silver = [
            f"{code}_{substance}" for code, substance in zip(codes_stations, substances)
        ]

        # 📘 Sauvegarde des métadonnées par année
        metadonnees[annee] = {
            colonne: {
                "code_station": code,
                "nom_station": nom,
                "polluant": substance,
                "unite": unite,
            }
            for colonne, code, nom, substance, unite in zip(
                colonnes_silver,
                codes_stations,
                noms_stations,
                substances,
                unites,
            )
        }

        # 📊 Lecture des données de mesures (on ignore les 6 premières lignes)
        donnees = pd.read_csv(fichier_brut, skiprows=6)

        # 🔄 Renommage des colonnes de mesure
        dictionnaire_renommage = {
            donnees.columns[i + 1]: colonnes_silver[i]
            for i in range(len(colonnes_silver))
        }
        donnees.rename(columns=dictionnaire_renommage, inplace=True)

        # 🕒 Conversion de la colonne datetime
        donnees[donnees.columns[0]] = pd.to_datetime(
            donnees[donnees.columns[0]], errors="coerce"
        )
        donnees.rename(columns={donnees.columns[0]: "datetime"}, inplace=True)

        # 🔢 Conversion des valeurs de mesure en float
        for colonne in colonnes_silver:
            donnees[colonne] = pd.to_numeric(donnees[colonne], errors="coerce")

        # 💾 Sauvegarde du fichier Silver nettoyé
        fichier_silver = os.path.join(CHEMIN_SILVER, f"{annee}_CO_silver.csv")
        donnees.to_csv(fichier_silver, index=False)
        print(f"✅ Fichier Silver enregistré : {fichier_silver}")

# 💾 Sauvegarde des métadonnées globales au format JSON
fichier_metadonnees = os.path.join(CHEMIN_SILVER, "CO_metadata.json")
with open(fichier_metadonnees, "w", encoding="utf-8") as f:
    json.dump(metadonnees, f, ensure_ascii=False, indent=2)

print(f"✅ Métadonnées enregistrées : {fichier_metadonnees}")
