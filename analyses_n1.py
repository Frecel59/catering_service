import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from Data_cleaning.Clean_data import clean_file_in_folder
from Data_cleaning.Clean_data_snack import clean_file_in_folder_snack
from Data_cleaning.df_global import merged_df

def format_date_in_french(date):
    # Définir les noms des mois en français
    mois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']

    # Formater la date en utilisant le format souhaité
    return f"{date.day} {mois[date.month - 1]} {date.year}"

def main():
    # Charger le contenu du fichier CSS
    with open('style.css', 'r') as css_file:
        css = css_file.read()

    # Afficher le contenu CSS dans la page Streamlit
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    #########################################################################
    #########################################################################

    st.title("Analyses N-1")

    #########################################################################
    ############################## EN COURS #################################
    #########################################################################

    brasserie_start_a = clean_file_in_folder().Date.min().strftime("%d/%m/%Y")
    brasserie_end_a = clean_file_in_folder().Date.max().strftime("%d/%m/%Y")
    snack_start_a = clean_file_in_folder_snack().Date.min().strftime("%d/%m/%Y")
    snack_end_a = clean_file_in_folder_snack().Date.max().strftime("%d/%m/%Y")

    st.write("")
    formatted_period_brasserie_a = f"Brasserie données disponibles : du {brasserie_start_a} au {brasserie_end_a}"
    formatted_period_snack_a = f"Snack données disponibles : du {snack_start_a} au {snack_end_a}"
    st.markdown(f'<p class="period-text">{formatted_period_brasserie_a}</br>{formatted_period_snack_a}</p>', unsafe_allow_html=True)

    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    #########################################################################
    ############# CHAMPS INPUT POUR LE CHOIX DES PERIODES ###################
    #########################################################################

    # Appeler la fonction merged_df pour obtenir les données avec météo
    df2 = merged_df()

    st.markdown(f'<p class="period-text">Choississez une période N</p>', unsafe_allow_html=True)

    # Créer une mise en page en colonnes
    col_1, col_2 = st.columns(2)

    # Ajouter le widget date_input dans la première colonne
    with col_1:
        start_date_a = st.date_input("Date de départ", datetime((df2["Date"].max()).year - 1, 11, 1), key="start_date_input_a", format="DD/MM/YYYY") # 01/11 + année -1 de date max
        formatted_start_date_a = format_date_in_french(start_date_a)

    with col_2:
        end_date_a = st.date_input("Date de fin", df2["Date"].max(), key="end_date_input_a", format="DD/MM/YYYY")
        formatted_end_date_a = format_date_in_french(end_date_a)

    st.markdown(f'<p class="period-text">Choississez une période N-1</p>', unsafe_allow_html=True)

    # Créer une mise en page en colonnes
    col_3, col_4 = st.columns(2)

    # Ajouter le widget date_input dans la première colonne
    with col_3:
        start_date_a2 = st.date_input("Date de départ", datetime((df2["Date"].max()).year - 1, 11, 1) - timedelta(days=365), key="start_date_input_a2", format="DD/MM/YYYY") # 01/11 + année -1 de date max
        formatted_start_date_a2 = format_date_in_french(start_date_a2)

    with col_4:
        end_date_a2 = st.date_input("Date de fin", df2["Date"].max() - timedelta(days=365), key="end_date_input_a2", format="DD/MM/YYYY")
        formatted_end_date_a2 = format_date_in_french(end_date_a2)

    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    #########################################################################
    ############# AFFICHAGE DU BILAN EN FONCTION JOURS ET SERVICES ##########
    #########################################################################

    # Formater les dates au format "dd-mm-yyyy"
    formatted_start_date_a = start_date_a.strftime("%d/%m/%Y")
    formatted_end_date_a = end_date_a.strftime("%d/%m/%Y")
    formatted_start_date_a2 = start_date_a2.strftime("%d/%m/%Y")
    formatted_end_date_a2 = end_date_a2.strftime("%d/%m/%Y")

    st.write("")
    formatted_period_a = f"Période N : du {formatted_start_date_a} au {formatted_end_date_a}"
    formatted_period_a2 = f"Période N-1 : du {formatted_start_date_a2} au {formatted_end_date_a2}"
    st.markdown(f'<p class="period-text2">{formatted_period_a}</br>{formatted_period_a2}</p>', unsafe_allow_html=True)



    # Liste des jours de la semaine
    jours_semaine_a = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

    # Créez un dictionnaire pour stocker les moments sélectionnés pour chaque jour
    jours_moments_selectionnes_a = {}

    # Utilisez un expander pour afficher les cases à cocher
    with st.expander("Sélectionnez les jours et services"):
        for jour in jours_semaine_a:
            jours_moments_selectionnes_a[jour] = []

            # Les cases sont cochées par défaut
            midi = st.checkbox(f'{jour} - Midi', key=f'{jour}_midi', value=True)
            soir = st.checkbox(f'{jour} - Soir', key=f'{jour}_soir', value=True)

            # Si la case "Midi" est cochée, ajoutez "Midi" à la liste des moments sélectionnés pour ce jour
            if midi:
                jours_moments_selectionnes_a[jour].append("Midi")

            # Si la case "Soir" est cochée, ajoutez "Soir" à la liste des moments sélectionnés pour ce jour
            if soir:
                jours_moments_selectionnes_a[jour].append("Soir")

    # Filtrer les données en fonction des jours sélectionnés
    filtered_a = df2[df2['Jour'].isin([jour for jour, _ in jours_moments_selectionnes_a.items()])]




    # # Filtrer le DataFrame en fonction des dates choisies
    # filtered_df = df[(df["Date"] >= start_date_convert) & (df["Date"] <= end_date_convert)]





if __name__ == "__main__":
    main()
