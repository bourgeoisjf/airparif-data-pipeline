# Airparif Data Pipeline

## Présentation du projet

Ce projet a pour objectif de concevoir un **pipeline de données** permettant d’extraire, transformer et préparer des données de qualité de l’air issues des **API et jeux de données Open Data d’Airparif**.

Le pipeline est pensé dans une logique **Data Engineering**, avec une séparation claire des responsabilités :
- ingestion des données brutes,
- transformation et normalisation,
- préparation des données pour une utilisation analytique ultérieure (bases de données, visualisation, reporting).

Le projet est volontairement construit de manière progressive afin de documenter chaque étape du cycle de vie de la donnée.

---

## Sources de données

Les données utilisées proviennent de la plateforme Open Data d’Airparif :

- Indices de qualité de l’air (prévisions et temps réel) via l’API Airparif
- Données historiques de concentration de polluants (exemple : Monoxyde de carbone – CO) via les jeux de données ArcGIS Open Data

Les données historiques sont considérées comme **immutables** (un fichier par année), tandis que les données de prévision et temps réel sont **dynamiques**.

---

## Architecture du projet

Le projet suit une architecture en couches inspirée des bonnes pratiques du Data Engineering.

### Structure des dossiers
```bash
airparif-data-pipeline/
│
├── data/
│   ├── raw/
│   │   ├── forecast/
│   │   │   └── paris/
│   │   │       └── paris_forecast.json
│   │   │
│   │   ├── realtime/
│   │   │   └── paris/
│   │   │       └── paris_realtime.json
│   │   │
│   │   └── historical/
│   │       └── co/
│   │           ├── 2023_CO.csv
│   │           ├── 2024_CO.csv
│   │           └── 2025_CO.csv
│   │
│   └── silver/
│       └── historical/
│           └── co/
│               ├── 2023_CO_silver.csv
│               ├── 2024_CO_silver.csv
│               ├── 2025_CO_silver.csv
│               └── CO_metadata.json
│
├── src/
│   ├── extract/
│   │   ├── airparif_extract_forecast_paris.py
│   │   ├── airparif_extract_realtime_paris.py
│   │   └── airparif_extract_historical_co.py
│   │
│   ├── transform/
│   │   └── airparif_transform_co.py
│   │
│   └── run_pipeline.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md

```

---

## Couches de données

### Bronze (Raw)

La couche Bronze contient les données telles qu’elles sont fournies par la source :
- fichiers JSON issus des API (prévisions et temps réel),
- fichiers CSV historiques téléchargés depuis l’Open Data Airparif.

Aucune modification n’est appliquée à ce stade.

---

### Silver

La couche Silver contient des données :
- nettoyées,
- typées correctement (datetime, float),
- avec des noms de colonnes normalisés,
- prêtes à être analysées ou chargées dans une base de données.

Pour les données historiques de CO :
- les métadonnées présentes dans les premières lignes des fichiers CSV sont extraites,
- les données de mesure sont séparées des métadonnées,
- un fichier JSON de métadonnées est généré afin de conserver les informations descriptives (station, substance, unité).

---

## Scripts existants

### Extraction

- `airparif_extract_forecast_paris.py`  
  Extraction des prévisions de qualité de l’air pour Paris.

- `airparif_extract_realtime_paris.py`  
  Extraction des données temps réel pour Paris.

- `airparif_extract_historical_co.py`  
  Téléchargement des fichiers historiques annuels de CO (processus ponctuel, non automatisé).

---

### Transformation

- `airparif_transform_co.py`  
  Transformation des fichiers historiques de CO :
  - suppression des lignes de métadonnées,
  - standardisation des noms de colonnes,
  - conversion des types,
  - génération d’un fichier de métadonnées structuré.

---

## Orchestration

Le fichier `run_pipeline.py` constitue une première version d’orchestration du pipeline.  
À ce stade, il se limite à l’exécution des scripts d’extraction.

Il sera enrichi progressivement au fil de l’évolution du projet.

---

## Objectifs pédagogiques et professionnels

Ce projet a pour objectifs :
- de démontrer une compréhension claire des concepts de Data Engineering,
- de mettre en œuvre une architecture en couches (Bronze / Silver),
- de travailler avec des API et des jeux de données Open Data,
- de documenter un pipeline de données réaliste et reproductible.

Les prochaines étapes incluront l’intégration d’une base de données relationnelle (PostgreSQL) et la création de tables analytiques.

---

## Technologies utilisées

- Python
- Pandas
- Requests
- APIs REST
- Open Data (Airparif / ArcGIS)

---

## Auteur

Projet développé à des fins de montée en compétences en Data Engineering et de constitution d’un portfolio technique.
