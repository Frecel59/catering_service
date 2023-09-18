import os
import streamlit as st
from gcp import get_storage_client
from google.cloud.exceptions import NotFound
from google.cloud import storage

def upload_to_bucket(file, folder_name):
    client, bucket = get_storage_client()

    # Construire le nom de fichier complet avec le préfixe du dossier.
    filename = os.path.join(folder_name, file.name)

    # Télécharge le fichier dans le bucket.
    blob = bucket.blob(filename)
    blob.upload_from_file(file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    print(f"File {file.name} uploaded to {filename}.")

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

if __name__ == "__main__":
    main()
