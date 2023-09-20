# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from tabulate import tabulate
import io
import matplotlib.pyplot as plt

# Importation des fonctions personnalisées depuis d'autres fichiers Python
from gcp import get_storage_client
from Analyses.graph import show_grouped_data
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
    display_icon("Analyses", "Analyses d'une période")

    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    #########################################################################
    ############# CHAMPS INPUT POUR LE CHOIX DE LA PERIODE ##################
    #########################################################################
    # Début de la section pour le bilan en fonction des jours et services

    def get_df_from_gcp():
        client, bucket = get_storage_client()

        # Chemin vers votre fichier dans le bucket
        blob_path = "COVERS_BRASSERIE_DF_FINALE/df_finale.xlsx"
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


    #########################################################################
    ############# AFFICHAGE DU BILAN EN FONCTION JOURS ET SERVICES ##########
    #########################################################################

    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    # Afficher le tableau formaté
    # Formater les dates au format "dd-mm-yyyy"
    formatted_start_date = start_date.strftime("%d/%m/%Y")
    formatted_end_date = end_date.strftime("%d/%m/%Y")

    st.write("")
    formatted_period = f"Bilan de la période : du {formatted_start_date} au \
        {formatted_end_date}"
    st.markdown(f'<p class="period-text2">{formatted_period}</p>', \
        unsafe_allow_html=True)



    # Liste des jours de la semaine
    jours_semaine = ['Lundi',
                     'Mardi',
                     'Mercredi',
                     'Jeudi',
                     'Vendredi',
                     'Samedi',
                     'Dimanche']

    # Créez un dico pour stocker les moments sélectionnés pour chaque jour
    jours_moments_selectionnes = {}

    # Utilisez un expander pour afficher les cases à cocher
    with st.expander("Sélectionnez les jours et services"):
        for jour in jours_semaine:
            jours_moments_selectionnes[jour] = []

            # Les cases sont cochées par défaut
            midi = st.checkbox(f'{jour} - Midi', key=f'{jour}_midi', value=True)
            soir = st.checkbox(f'{jour} - Soir', key=f'{jour}_soir', value=True)

            # Si la case "Midi" est cochée, ajoutez "Midi" à la liste \
                # des moments sélectionnés pour ce jour
            if midi:
                jours_moments_selectionnes[jour].append("Midi")

            # Si la case "Soir" est cochée, ajoutez "Soir" à la liste \
                # des moments sélectionnés pour ce jour
            if soir:
                jours_moments_selectionnes[jour].append("Soir")

    # Filtrer les données en fonction des jours sélectionnés
    filtered_vsd = filtered_df[filtered_df['Jour'].isin([jour for jour, \
        _ in jours_moments_selectionnes.items()])]


    # Appel de la fonction analyses_bilan et récupération des deux DataFrames
    result_df, result_df1 = analyses_bilan(jours_moments_selectionnes, \
        filtered_vsd)

    # Afficher le DataFrame en occupant toute la largeur de la page
    st.table(result_df1)


    # Utilisez la fonction generate_excel_report pour générer le rapport Excel
    excel_output = generate_excel_report(result_df, formatted_start_date, \
        formatted_end_date)

    # Utilisez st.download_button pour afficher un bouton de téléchargement
    st.download_button(
        label=f"Télécharger au format Excel",
        data=excel_output,
        file_name=f"bilan_{formatted_start_date}_{formatted_end_date}.xlsx",
        key="download_results"
    )



    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    #########################################################################
    ################### GRAPHIQUE AVEC WIDGETS STREAMLIT ####################
    #########################################################################

    # Convertir la colonne 'date' en datetime
    graph_df = filtered_df.copy()
    graph_df['Date'] = pd.to_datetime(graph_df['Date'])


    st.markdown(f'<p class="period-text2">Analyse journalière</p>' , \
        unsafe_allow_html=True)

    st.markdown(f'<p class="period-text">Choississez vos filtres</p>' , \
        unsafe_allow_html=True)

    # Créer les widgets
    # Créer une mise en page en colonnes
    col1, col2, col3, col4, col5 = st.columns(5)

    # Ajouter le widget date_input dans la première colonne
    with col2:
        group_by_option = st.selectbox('Trier par :', [
            'Jour',
            'Mois et Jour'])

    with col3:
        data_type_option = st.selectbox('Type de données :', [
            'Nbr total couv. 12h',
            'Nbr total couv. 19h',
            'Nbr total couv.',
            'Additions 12h',
            'Additions 19h',
            'Total additions'
            ])


    if group_by_option == 'Mois et Jour':
        unique_months = graph_df['Date'].dt.to_period("M").unique() \
            .strftime('%m/%Y').tolist()
        with col4:
            month_option = st.selectbox('Mois :', unique_months)

    else:
        month_option = None

    # Divisez la page en 3 colonnes: [1, 2, 1]
    left_col, center_col, right_col = st.columns([1, 2, 1])

    # Placez le graphique dans la colonne du centre (center_col)
    with center_col:
    # Afficher le graphique en fonction des widgets
        show_grouped_data(group_by_option, data_type_option, group_by_option, \
            data_type_option, month_option, graph_df)

    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    ####################################################################
    ######### AFFICHAGE DU DATAFRAME AVEC POSSIBILITE DE FILTRE ########
    ####################################################################

    st.markdown(f'<p class="period-text">Données avec météo pour la période \
        sélectionnée :</p>', unsafe_allow_html=True)

    # Convertissez les colonnes "Date" et "date" en datetime
    filtered_table = filtered_df.assign(Date=pd.to_datetime(filtered_df['Date']))


    # Formatez la colonne "Date" pour l'afficher au format "dd-mm-yyyy"
    filtered_table = filtered_table.assign(Date=filtered_table['Date']\
        .dt.strftime("%d-%m-%Y"))


    # Ajoutez des cases à cocher pour permettre à l'utilisateur de \
        # sélectionner les colonnes à afficher
    selected_columns = st.multiselect(
        'Sélectionnez les colonnes à afficher',
        options=filtered_table.columns,
        default=filtered_table.columns.tolist() # Afficher tous par défaut
    )

    # Filtrer le DataFrame en fonction des colonnes sélectionnées
    filtered_table = filtered_table[selected_columns]

    # Affichez le DataFrame filtré
    st.dataframe(filtered_table)


    # Créer un objet BytesIO pour stocker les données Excel
    output2 = io.BytesIO()

    # Utiliser Pandas pour sauvegarder le DataFrame au format Excel
    with pd.ExcelWriter(output2, engine='xlsxwriter') as writer:
        filtered_table.to_excel(writer, sheet_name='Sheet1', index=False)

    # Définir le point de départ pour la lecture
    output2.seek(0)

    # Utilisez st.download_button pour afficher un bouton de téléchargement
    st.download_button(
        label=f"Télécharger au format Excel",
        data=output2,
        file_name=f"donnees_{formatted_start_date}_{formatted_end_date}.xlsx",
        key="download_results2"
        )

    footer.display()

    return filtered_df





if __name__ == "__main__":
    print(main().columns)
