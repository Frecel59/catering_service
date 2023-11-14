import pandas as pd
import numpy as np
import re
import streamlit as st
from google.cloud import storage
from io import BytesIO
from gcp import get_storage_client

def clean_file_ventes_snack(excel_file_stream):
    df = pd.read_excel(excel_file_stream, engine='openpyxl')

    # Supprimer les lignes 0 à 9
    df.drop(range(9), inplace=True)

    # Supressions des colonnes inutiles
    cols_to_drop = ['Rapport ventes Cédric', 'Unnamed: 3', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11', 'PASINO SAINT AMAND', 'Unnamed: 14', 'Unnamed: 15']
    df = df.drop(columns=cols_to_drop)

    # Création d'un dictionnaire
    new_column_names = {
        'Unnamed: 0': 'Année',
        'Unnamed: 2': 'Mois',
        'Unnamed: 4': 'Jour',
        'Unnamed: 6': 'Catégorie',
        'Unnamed: 8': 'Produit',
        'Unnamed: 13': 'Quantité',
        'Unnamed: 16': 'Prix'
    }

    # Renommer les colonnes en utilisant le dictionnaire de correspondance
    df.rename(columns=new_column_names, inplace=True)

    # Remplacez la valeur "Année" par NaN
    df.replace("Année", np.nan, inplace=True)

    # Remplissage des valeurs NaN dans la colonne 'Année' - on recopie la valeur au dessus sur les lignes du dessous jusqu'à la prochaine valeur année - pareil pour Mois, Jour et Catégorie
    df['Année'] = df['Année'].fillna(method='ffill')
    df['Année'] = df['Année'].astype(str)

    df['Mois'] = df['Mois'].fillna(method='ffill')
    df['Mois'] = df['Mois'].astype(str)

    df['Jour'] = df['Jour'].fillna(method='ffill')
    df['Jour'] = df['Jour'].astype(str)

    df['Catégorie'] = df['Catégorie'].fillna(method='ffill')
    df['Catégorie'] = df['Catégorie'].astype(str)

    # Suppression des lignes où 'Produit' est NaN
    df = df.dropna(subset=['Produit'])

    # Extraire les chiffres de la colonne "Mois"
    df.loc[:, 'Mois'] = df['Mois'].apply(lambda x: int(re.findall(r'\d+', str(x))[0]) if pd.notna(x) else x)

    # Convertir les colonnes en entier
    df.loc[:, "Année"] = df["Année"].astype(str).str.rstrip('.0').astype(int)
    df.loc[:, "Jour"] = df["Jour"].astype(str).str.rstrip('.0').astype(int)
    df.loc[:, 'Mois'] = df['Mois'].astype(int)

    # ajouter colonne date
    df.loc[:, 'Date'] = pd.to_datetime(df[['Année', 'Mois', 'Jour']].astype(str).agg('-'.join, axis=1))

    # Réorganisez l'ordre des colonnes
    df = df[['Date', 'Année', 'Mois', 'Jour', 'Catégorie', 'Produit', 'Quantité', 'Prix']]

    # On supprime les colonnes inutiles
    cols_to_drop2 = ['Année', 'Mois', 'Jour']
    df = df.drop(columns=cols_to_drop2)

    # Supprimer les lignes où toutes les valeurs sont identiques
    df = df.drop_duplicates()

    return df

def clean_file_from_gcs_ventes_snack(blob):
    """Lire le fichier excel et retourner un dataframe clean."""
    in_mem_file = BytesIO()
    blob.download_to_file(in_mem_file)
    df = clean_file_ventes_snack(in_mem_file)
    in_mem_file.close()

    return df


def clean_files_in_bucket_ventes_snack():
    all_dataframes = []

    client, bucket = get_storage_client()

    # List all the blobs in COVERS_BRASSERIE folder
    blobs = bucket.list_blobs(prefix="VENTES_SNACK/")

    for blob in blobs:
        if blob.name.endswith('.xls'):
            df = clean_file_from_gcs_ventes_snack(blob)
            all_dataframes.append(df)

    df = pd.concat(all_dataframes, ignore_index=True)

    return df

if __name__ == '__main__':
    print(clean_files_in_bucket_ventes_snack().Date.min())
