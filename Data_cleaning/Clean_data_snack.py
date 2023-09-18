import pandas as pd
import os
from google.cloud import storage
from io import BytesIO
from gcp import get_storage_client

def clean_file_snack(excel_file_stream):
    df = pd.read_excel(excel_file_stream, engine='openpyxl')

    # Supprimer les lignes 0 à 9
    df.drop(range(10), inplace=True)

    # Liste des noms de colonnes à supprimer
    colonnes_a_supprimer = [
        'Rapport Brasserie Cedric',
        'Unnamed: 6',
        'Unnamed: 8',
        'PASINO SAINT AMAND',
        'Unnamed: 11',
        'Unnamed: 13'
    ]

    # Supprimer les colonnes spécifiées
    df.drop(columns=colonnes_a_supprimer, inplace=True)

    # Création d'un dictionnaire de correspondance
    new_column_names = {
        'Unnamed: 0': 'Date',
        'Unnamed: 2': 'Diner_Covers_sales',
        'Unnamed: 3': 'Diner_Price_sales',
        'Unnamed: 4': 'Diner_Covers_intern',
        'Unnamed: 5': 'Diner_Price_intern',
        'Unnamed: 7': 'Dej_Covers_sales',
        'Unnamed: 9': 'Dej_Price_sales',
        'Unnamed: 12': 'Dej_Covers_intern',
        'Unnamed: 14': 'Dej_Price_intern'
    }

    # Renommer les colonnes en utilisant le dictionnaire de correspondance
    df.rename(columns=new_column_names, inplace=True)

    # Remplacer les NaN par 0
    df = df.fillna(0)

    # Convertir la colonne "Date" au format date
    df["Date"] = pd.to_datetime(df["Date"], format='%d/%m/%Y')

    return df

def clean_file_from_gcs_snack(blob):
    """Lire le fichier excel et retourner un dataframe clean."""
    in_mem_file = BytesIO()
    blob.download_to_file(in_mem_file)
    df = clean_file_snack(in_mem_file)
    in_mem_file.close()

    return df

def clean_files_in_bucket_snack():
    all_dataframes = []

    client, bucket = get_storage_client()

    # List all the blobs in COVERS_BRASSERIE folder
    blobs = bucket.list_blobs(prefix="COVERS_SNACK/")

    for blob in blobs:
        if blob.name.endswith('.xlsx'):
            df = clean_file_from_gcs_snack(blob)
            all_dataframes.append(df)

    df = pd.concat(all_dataframes, ignore_index=True)

    return df

if __name__ == '__main__':
    print(clean_files_in_bucket_snack().Date.min())
