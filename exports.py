import os
import io
import pandas as pd
import streamlit as st
from gcp import get_storage_client
from google.cloud.exceptions import NotFound
from google.cloud import storage

from Data_cleaning.df_global import merged_df
from Data_cleaning.Clean_data import clean_files_in_bucket
from Data_cleaning.Clean_data_snack import clean_files_in_bucket_snack

def upload_to_bucket(file, folder_name):
    client, bucket = get_storage_client()

    # Construire le nom de fichier complet avec le préfixe du dossier.
    filename = os.path.join(folder_name, file.name)

    # Télécharge le fichier dans le bucket.
    blob = bucket.blob(filename)
    blob.upload_from_file(file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    print(f"File {file.name} uploaded to {filename}.")

def save_final_dataframe():
    df_final = merged_df()
    # Convertir le DataFrame directement en un objet BytesIO pour éviter de le sauvegarder localement
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_final.to_excel(writer, index=False)
    output.seek(0)

    # Créer un objet de fichier semblable avec le contenu du BytesIO et le nom souhaité
    final_file = type('', (object,), {'name': 'df_finale.xlsx', 'read': output.read, 'seek': output.seek, 'tell': output.tell})()

    # Réinitialisez la position à 0 pour être sûr
    final_file.seek(0)

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

    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    # Obtenir les données des 2 def
    brasserie_data = clean_files_in_bucket()
    snack_data = clean_files_in_bucket_snack()

    # Extraire les dates de début et de fin à partir des données obtenues
    brasserie_start = brasserie_data.Date.min().strftime("%d/%m/%Y")
    brasserie_end = brasserie_data.Date.max().strftime("%d/%m/%Y")
    snack_start = snack_data.Date.min().strftime("%d/%m/%Y")
    snack_end = snack_data.Date.max().strftime("%d/%m/%Y")

    st.write("")

    formatted_period_brasserie = f"Brasserie données disponibles : du \
        {brasserie_start} au {brasserie_end}"

    formatted_period_snack = f"Snack données disponibles : du \
        {snack_start} au {snack_end}"

    st.markdown(f'<p class="period-text">{formatted_period_brasserie}</br> \
        {formatted_period_snack}</p>', unsafe_allow_html=True)

    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    # Upload pour Brasserie
    brasserie_file = st.file_uploader("Choisissez un fichier Brasserie (.xlsx)", type=["xlsx"])
    if brasserie_file:
        upload_to_bucket(brasserie_file, "COVERS_BRASSERIE")
        st.success(f"Fichier {brasserie_file.name} téléchargé avec succès dans le dossier BRASSERIE.")

    # Upload pour Snack
    snack_file = st.file_uploader("Choisissez un fichier Snack (.xlsx)", type=["xlsx"])
    if snack_file:
        upload_to_bucket(snack_file, "COVERS_SNACK")
        st.success(f"Fichier {snack_file.name} téléchargé avec succès dans le dossier SNACK.")

    # Après avoir téléchargé les fichiers Brasserie ou Snack, mettez à jour le dataframe final
    if brasserie_file or snack_file:
        save_final_dataframe()

if __name__ == "__main__":
    main()
