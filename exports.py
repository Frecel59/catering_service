import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from config import Config
from gcp import get_storage_client

load_dotenv()

# Utilisez la fonction get_storage_client pour obtenir le client et le bucket
client, bucket = get_storage_client()

def main():
    # Charger le contenu du fichier CSS personnalisé
    with open('style.css', 'r') as css_file:
        css = css_file.read()

    # Incorporer le CSS personnalisé dans l'application
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    st.title("Exportations des Fichiers")
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    # Ajoutez un champ d'envoi de fichiers pour le fichier Brasserie
    st.header("Fichier Brasserie")
    uploaded_file_brasserie = st.file_uploader("Sélectionnez un fichier Excel (xlsx) à envoyer (Brasserie)", type=["xlsx"])

    if uploaded_file_brasserie:
        file_name = uploaded_file_brasserie.name
        target_folder = "COVERS_BRASSERIE"  # Vous pouvez déterminer le dossier cible en fonction des préférences de l'utilisateur

        # Lire le fichier Excel en tant que DataFrame
        df = pd.read_excel(uploaded_file_brasserie)

        # Créez un objet blob pour le fichier dans le bucket
        blob = bucket.blob(f"{target_folder}/{file_name}")

        # Envoyez le DataFrame directement au blob au format CSV
        csv_data = df.to_csv(index=False)
        blob.upload_from_string(csv_data, content_type="application/vnd.ms-excel")  # Spécifiez le type MIME pour les fichiers Excel

        st.success(f"Le fichier {file_name} (Brasserie) a été envoyé avec succès dans le dossier {target_folder} du bucket GCP.")

    # Ajoutez un champ d'envoi de fichiers pour le fichier Snack
    st.header("Fichier Snack")
    uploaded_file_snack = st.file_uploader("Sélectionnez un fichier Excel (xlsx) à envoyer (Snack)", type=["xlsx"])

    if uploaded_file_snack:
        file_name = uploaded_file_snack.name
        target_folder = "COVERS_SNACK"  # Vous pouvez déterminer le dossier cible en fonction des préférences de l'utilisateur

        # Lire le fichier Excel en tant que DataFrame
        df = pd.read_excel(uploaded_file_snack)

        # Créez un objet blob pour le fichier dans le bucket
        blob = bucket.blob(f"{target_folder}/{file_name}")

        # Envoyez le DataFrame directement au blob au format CSV
        csv_data = df.to_csv(index=False)
        blob.upload_from_string(csv_data, content_type="application/vnd.ms-excel")  # Spécifiez le type MIME pour les fichiers Excel

        st.success(f"Le fichier {file_name} (Snack) a été envoyé avec succès dans le dossier {target_folder} du bucket GCP.")

if __name__ == "__main__":
    main()
