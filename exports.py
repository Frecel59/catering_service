import os
import io
import pandas as pd
import streamlit as st
from gcp import get_storage_client
from google.cloud.exceptions import NotFound
from google.cloud import storage

from Data_cleaning.merged_data import merged_data  # Import de la fonction merged_data

def upload_to_bucket(file, folder_name):
    client, bucket = get_storage_client()

    # Construire le nom de fichier complet avec le préfixe du dossier.
    filename = os.path.join(folder_name, file.name)

    # Télécharge le fichier dans le bucket.
    blob = bucket.blob(filename)
    blob.upload_from_file(file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    print(f"File {file.name} uploaded to {filename}.")

def save_final_dataframe():
    df_final = merged_data()
    # Convertir le DataFrame directement en un objet BytesIO pour éviter de le sauvegarder localement
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_final.to_excel(writer, index=False)
    output.seek(0)

    # Créer un objet de fichier semblable avec le contenu du BytesIO et le nom souhaité
    final_file = type('', (object,), {'name': 'df_finale.xlsx', 'read': output.read})()

    # Téléchargez ce "fichier" dans le bucket
    upload_to_bucket(final_file, "COVERS_BRASSERIE_DF_FINALE")

def main():
    # Charger le contenu du fichier CSS
    with open('style.css', 'r') as css_file:
        css = css_file.read()

    # Afficher le contenu CSS dans la page Streamlit
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    #########################################################################
    #########################################################################

    st.title("Exportations des fichiers")

    # Utiliser le séparateur horizontal
