# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io
import matplotlib.pyplot as plt
import plotly.express as px

# Importation des fonctions personnalisées depuis d'autres fichiers Python
from gcp import get_storage_client
from Analyses.bilan import analyses_bilan
from Analyses.excel_generation import generate_excel_report
import footer
from utils import display_icon


# Fonction pour formater une date en français
def format_date_in_french(date):
    # Liste des noms de mois en français
    mois = [
        'janvier',
        'février',
        'mars',
        'avril',
        'mai',
        'juin',
        'juillet',
        'août',
        'septembre',
        'octobre',
        'novembre',
        'décembre']

    # Formater la date au format "jour mois année"
    return f"{date.day} {mois[date.month - 1]} {date.year}"

# Fonction principale
def main():
    # Charger le contenu du fichier CSS
    with open('style.css', 'r') as css_file:
        css = css_file.read()

    # Afficher le contenu CSS dans la page Streamlit
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    #########################################################################
    #########################################################################

    # Afficher l'icône pour la page avec le titre personnalisé
    display_icon("Bilan ventes", "Bilan d'une période")

    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    #########################################################################
    ############# CHAMPS INPUT POUR LE CHOIX DE LA PERIODE ##################
    #########################################################################
    # Début de la section pour le bilan en fonction des jours et services

    def get_df_from_gcp():
        client, bucket = get_storage_client()

        # Chemin vers votre fichier dans le bucket
        blob_path = "DF_FINALE/COVERS_df_finale.xlsx"
        blob = bucket.blob(blob_path)

        # Téléchargez le fichier dans un objet en mémoire
        in_memory_file = io.BytesIO()
        blob.download_to_file(in_memory_file)
        in_memory_file.seek(0)

        # Lisez le fichier Excel dans un DataFrame
        df = pd.read_excel(in_memory_file)

        return df

    # Appeler la fonction get_df_from_gcp pour obtenir les données
    df_final = get_df_from_gcp()

    st.markdown(f'<p class="period-text">Choississez une période</p>' , \
        unsafe_allow_html=True)

    # Créer une mise en page en colonnes
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    # Ajouter le widget date_input dans la première colonne
    with col3:
        start_date = st.date_input("Date de départ", \
            datetime((df_final["Date"].max()).year - 1, 11, 1), \
            key="start_date_input", format="DD/MM/YYYY")
            # 01/11 + année -1 de date max
        formatted_start_date = format_date_in_french(start_date)

    with col4:
        end_date = st.date_input("Date de fin", df_final["Date"].max(), \
            key="end_date_input", format="DD/MM/YYYY")
        formatted_end_date = format_date_in_french(end_date)

    # Convertir les dates sélectionnées en objets datetime64[ns]
    start_date_convert = pd.to_datetime(start_date)
    end_date_convert = pd.to_datetime(end_date)

    # Filtrer le DataFrame en fonction des dates choisies
    filtered_df = df_final[(df_final["Date"] >= start_date_convert) & \
        (df_final["Date"] <= end_date_convert)]


    footer.display()






    return filtered_df





if __name__ == "__main__":
    print(main().columns)
