# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# Importation des fonctions personnalisées depuis d'autres fichiers Python
from gcp import get_storage_client
import footer
from utils import display_icon
from Analyses.bilan_n1 import analyses_bilan_n1

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
    display_icon("Analyses N-1", "Analyses d'une période par rapport à une autre")

    # Afficher le message "Développement en cours"
    st.markdown(
        """
        <div style="text-align:center;">
            <h2 style="color:red;">🚧 Développement en cours 🚧</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


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


    # Créer une mise en page en colonnes pour la période N et N-1
    col_N, col_N_1 = st.columns(2)

    # Période N
    with col_N:
        st.markdown(f'<p class="period-text">Choississez une période N</p>', \
            unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([0.1, 0.4, 0.4, 0.1])

        with col2:
            # Date de départ pour la période N
            start_date_a = st.date_input("Date de départ", datetime((df_final["Date"] \
                .max()).year - 1, 11, 1), key="start_date_input_a", \
                    format="DD/MM/YYYY")
            formatted_start_date_a = format_date_in_french(start_date_a)

        with col3:
            # Date de fin pour la période N
            end_date_a = st.date_input("Date de fin", df_final["Date"].max(), \
                key="end_date_input_a", format="DD/MM/YYYY")
            formatted_end_date_a = format_date_in_french(end_date_a)

    # Période N-1
    with col_N_1:
        st.markdown(f'<p class="period-text">Choississez une période N-1</p>', \
            unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([0.1, 0.4, 0.4, 0.1])

        with col2:
            # Date de départ pour la période N-1
            start_date_a2 = st.date_input("Date de départ",
                datetime((df_final["Date"].max()).year - 1, 11, 1) - timedelta(days=365),
                key="start_date_input_a2",
                format="DD/MM/YYYY")
            formatted_start_date_a2 = format_date_in_french(start_date_a2)

        with col3:
            # Date de fin pour la période N-1
            end_date_a2 = st.date_input("Date de fin", df_final["Date"].max() - \
                timedelta(days=365), key="end_date_input_a2", format="DD/MM/YYYY")
            formatted_end_date_a2 = format_date_in_french(end_date_a2)


        # Convertir les dates sélectionnées en objets datetime64[ns]
        start_date_convert_a = pd.to_datetime(start_date_a)
        end_date_convert_a = pd.to_datetime(end_date_a)
        start_date_convert_a2 = pd.to_datetime(start_date_a2)
        end_date_convert_a2 = pd.to_datetime(end_date_a2)

        # Filtrer le DataFrame en fonction des dates choisies
        df_a = df_final[(df_final["Date"] >= start_date_convert_a) & (df_final["Date"] \
            <= end_date_convert_a)]
        df_a2 = df_final[(df_final["Date"] >= start_date_convert_a2) & (df_final["Date"] \
            <= end_date_convert_a2)]

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
    formatted_period_a = f"Période N : du {formatted_start_date_a} au \
        {formatted_end_date_a}"
    formatted_period_a2 = f"Période N-1 : du {formatted_start_date_a2} au \
        {formatted_end_date_a2}"
    st.markdown(f'<p class="period-text2">{formatted_period_a}</br>\
        {formatted_period_a2}</p>', unsafe_allow_html=True)



    # Liste des jours de la semaine
    jours_semaine_a = ['Lundi',
                       'Mardi',
                       'Mercredi',
                       'Jeudi',
                       'Vendredi',
                       'Samedi',
                       'Dimanche']

    # Créez un dico pour stocker les moments sélectionnés pour chaque jour
    jours_moments_selectionnes_a = {}

    # Utilisez un expander pour afficher les cases à cocher
    with st.expander("Sélectionnez les jours et services"):
        for jour_a in jours_semaine_a:
            jours_moments_selectionnes_a[jour_a] = []

            # Les cases sont cochées par défaut
            midi_a = st.checkbox(f'{jour_a} - Midi', key=f'{jour_a}_midi_n1', value=True)
            soir_a = st.checkbox(f'{jour_a} - Soir', key=f'{jour_a}_soir_n1', value=True)


            # Si la case "Midi" est cochée, ajoutez "Midi" à la liste \
                # des moments sélectionnés pour ce jour
            if midi_a:
                jours_moments_selectionnes_a[jour_a].append("Midi")

            # Si la case "Soir" est cochée, ajoutez "Soir" à la liste \
                # des moments sélectionnés pour ce jour
            if soir_a:
                jours_moments_selectionnes_a[jour_a].append("Soir")

    # Filtrer les données en fonction des jours sélectionnés
    filtered_a = df_a[df_a['Jour'].isin([jour_a for jour_a, _ in \
        jours_moments_selectionnes_a.items()])]
    filtered_a2 = df_a2[df_a2['Jour'].isin([jour_a for jour_a, _ in \
        jours_moments_selectionnes_a.items()])]



    # Appel de la fonction analyses_bilan et récupération des deux DataFrames
    result_df_n1 = analyses_bilan_n1(jours_moments_selectionnes_a, \
        filtered_a, filtered_a2)


    st.dataframe(result_df_n1)


    footer.display()





if __name__ == "__main__":
    main()
