# SERVICE RESTAURATION

## Description
Analyse du nbr de couvert par service

## Installation
1. Clonez ce dépôt : `git clone https://github.com/Frecel59/catering_service.git`
2. Accédez au répertoire du projet : `cd catering_service`
3. Installez les dépendances : `pip install -r requirements.txt`

## Utilisation
Pour utiliser ce projet en local, exécutez la commande suivante : `streamlit run app.py`

## Liste des fichiers
Fichiers pour l'app
  1 - `app.py` : contient le menu
  2 - `exports.py` : permet l'envoie de fichier xlsx sur GCP
  3 - `analyses.py` : analyses des données selon une période déterminée
  4 - `predictions.py` :prédiction du nombre de couverts selon une période déterminée

Dossier Data_cleaning
  1 - `Clean_data.py` : importation et concatenation des fichiers brasseries
  2 - `Clean_data_snack.py` : importation et concatenation des fichiers snack
  3 - `merged_data.py` : merge des dataframe `Clean_data.py` et `Clean_data_snack.py` \
  par la date, avec somme des colonnes identiques, + ajouts de différentes colonnes
  4 - `API_meteo.py` : récupération des données météos historiques selon les dates \
  de début et fin de `merged_data.py`
  5 - `df_global.py` : intégration des données météos `API_meteo.py` dans `merged_data.py`

Dossier Analyses
  1 - `bilan.py` : création d'un bilan selon des dates choisies
  2 - `exel_generation.py` : exportation du bilan au format xlsx
  1 - `graph.py` : création d'un graphique dynamique avec filtres

## Statut du Projet
![En développement](https://img.shields.io/badge/Statut-En%20développement-brightgreen)

## Contact
Si vous avez des questions, veuillez contacter l'auteur à l'adresse suivante : \
[lecerf.c83@gmail.com](mailto:lecerf.c83@gmail.com).

## Rermerçiements
Je remerçie le responsable de la restauration pour sa confiance et sa disponibilité
