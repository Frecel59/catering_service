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
import footer

def main():
    # Charger le contenu du fichier CSS
    with open('style.css', 'r') as css_file:
        css = css_file.read()

    # Afficher le contenu CSS dans la page Streamlit
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    # Logo de l'entreprise
    st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhSUdVHlJsrGI4AIs3nUbSD-QPpnfiKOLVWw&usqp=CAU')

    st.title("Informations")

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

    formatted_period_brasserie = f"Brasserie données disponibles : du {brasserie_start} au {brasserie_end}"
    formatted_period_snack = f"Snack données disponibles : du {snack_start} au {snack_end}"

    st.markdown(f'<p class="period-text3">{formatted_period_brasserie}</br>{formatted_period_snack}</p>', unsafe_allow_html=True)

    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    # Lien vers le site de l'entreprise
    st.markdown('Pour plus d\'informations, visitez notre [site officiel](https://casino-saintamand.partouche.com/).')

    #########################################################################
    ############################## EN COURS #################################
    #########################################################################
    footer.display()

if __name__ == "__main__":
    main()
