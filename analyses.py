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
    display_icon("Bilan", "Bilan d'une période")

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

    # Créer une mise en page en colonnes
    col1, col2, col3 = st.columns([0.3, 0.4, 0.3])

    with col2:
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

    # Créer une mise en page en colonnes
    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])

    with col2:
        # Afficher le DataFrame en occupant toute la largeur de la page
        st.table(result_df1)


        # Utilisez la fonction generate_excel_report pour générer le rapport Excel
        excel_output = generate_excel_report(result_df, formatted_start_date, \
            formatted_end_date, jours_moments_selectionnes)

        # Utilisez st.download_button pour afficher un bouton de téléchargement
        st.download_button(
            label=f"Télécharger au format Excel",
            data=excel_output,
            file_name=f"bilan_{formatted_start_date}_{formatted_end_date}.xlsx",
            key="download_results"
        )



    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)



    ####################################################################
    ######### AFFICHAGE DU DATAFRAME AVEC POSSIBILITE DE FILTRE ########
    ####################################################################

    st.markdown(f'<p class="period-text2">Ensembles des données pour la période \
        sélectionnée</p>', unsafe_allow_html=True)

    # Convertissez les colonnes "Date" et "date" en datetime
    filtered_table = filtered_df.assign(Date=pd.to_datetime(filtered_df['Date']))


    # Formatez la colonne "Date" pour l'afficher au format "dd-mm-yyyy"
    filtered_table = filtered_table.assign(Date=filtered_table['Date']\
        .dt.strftime("%d-%m-%Y"))


    # Créer une mise en page en colonnes
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])

    # Ajoutez une case à cocher pour permettre à l'utilisateur de sélectionner les colonnes à afficher
    # Cela ira dans la colonne 2 (milieu)
    with col2:
        selected_columns = st.multiselect(
            'Sélectionnez les colonnes à afficher',
            options=filtered_table.columns,
            default=filtered_table.columns.tolist()  # Afficher tous par défaut
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

    # Créer une mise en page en colonnes
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])

    with col2:
        # Utilisez st.download_button pour afficher un bouton de téléchargement
        st.download_button(
            label=f"Télécharger au format Excel",
            data=output2,
            file_name=f"donnees_{formatted_start_date}_{formatted_end_date}.xlsx",
            key="download_results2"
            )


    df = filtered_vsd


    # 1. Analyse des couverts
    st.title("1. Analyse des couverts")

    df_report = df

    days_order = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    df_report['Jour'] = pd.Categorical(df_report['Jour'], categories=days_order, ordered=True)


    color_map_bar = {
        "Nbr couv. 12h": "#FFA726",
        "Nbr couv. 19h": "#5C6BC0",
        "Nbr couv. off 12h": "#AB47BC",
        "Nbr couv. off 19h": "#26A69A",
        "Nbr total couv. 19h": "#5C6BC0",
        "Nbr total couv. 12h": "#FFA726",
        "Additions 12h": "#FFA726",
        "Additions 19h": "#5C6BC0",
        "Total additions": "#5C6BC0",
        "Panier moyen 12h": "#FFA726",
        "Panier moyen 19h": "#5C6BC0",
        "Nbr serveurs 12h": "#FFA726",
        "Nbr serveurs 19h": "#5C6BC0",
    }
    # Création des colonnes
    col1, col2 = st.columns(2)

    # Graphique dans la colonne 1: Total des couverts payants
    with col1:
        st.markdown("### Nbr total de couverts (facturés)")
        fig = px.bar(
            df_report.groupby('Jour')[['Nbr couv. 12h', 'Nbr couv. 19h']].sum().reset_index(),
            x='Jour',
            y=['Nbr couv. 12h', 'Nbr couv. 19h'],
            color_discrete_map=color_map_bar
        )
        st.plotly_chart(fig)


    # Graphique dans la colonne 2: Total des couverts offerts
    with col2:
        st.markdown("### Nbr total de couverts (offerts)")
        fig = px.bar(
            df_report.groupby('Jour')[['Nbr couv. off 12h', 'Nbr couv. off 19h']].sum().reset_index(),
            x='Jour',
            y=['Nbr couv. off 12h', 'Nbr couv. off 19h'],
            color_discrete_map=color_map_bar
        )
        st.plotly_chart(fig)

    # Création de nouvelles colonnes
    col1, col2 = st.columns(2)

    # Graphique dans la colonne 1: Répartition des couverts offerts vs payants à 12h
    with col1:
        st.markdown("### Répartition des couverts offerts vs payants à 12h")
        fig = px.bar(
            df_report.groupby('Jour')[['Nbr couv. 12h', 'Nbr couv. off 12h']].sum().reset_index(),
            x='Jour',
            y=['Nbr couv. 12h', 'Nbr couv. off 12h'],
            color_discrete_map=color_map_bar
        )
        st.plotly_chart(fig)

    # Graphique dans la colonne 2: Répartition des couverts offerts vs payants à 19h
    with col2:
        st.markdown("### Répartition des couverts offerts vs payants à 19h")
        fig = px.bar(
            df_report.groupby('Jour')[['Nbr couv. 19h', 'Nbr couv. off 19h']].sum().reset_index(),
            x='Jour',
            y=['Nbr couv. 19h', 'Nbr couv. off 19h'],
            color_discrete_map=color_map_bar
        )
        st.plotly_chart(fig)

    # Graphique dans la colonne 1: Tendance des couverts à 12h
    with col1:
        st.markdown("### Tendance des couverts à 12h")
        fig = px.line(
            df_report,
            x='Date',
            y='Nbr total couv. 12h',
            color_discrete_sequence=[color_map_bar["Nbr total couv. 12h"]]
        )
        fig.update_xaxes(tickformat="%d-%m-%y")
        st.plotly_chart(fig)

    # Graphique dans la colonne 2: Tendance des couverts à 19h
    with col2:
        st.markdown("### Tendance des couverts à 19h")
        fig = px.line(
            df_report,
            x='Date',
            y='Nbr total couv. 19h',
            color_discrete_sequence=[color_map_bar["Nbr total couv. 19h"]]
        )
        fig.update_xaxes(tickformat="%d-%m-%y")
        st.plotly_chart(fig)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # 2. Analyse des additions
    st.title("2. Analyse des additions")

    # Création des colonnes
    col1, col2 = st.columns(2)

    # Graphique dans la colonne 1: Total des additions
    with col1:
        st.markdown("### Total des additions")
        fig = px.bar(
            df_report.groupby('Jour')[['Additions 12h','Additions 19h']].sum().reset_index(),
            x='Jour',
            y=['Additions 12h','Additions 19h'],
            color_discrete_map=color_map_bar
        )
        st.plotly_chart(fig)

    # Création des colonnes
    col1, col2 = st.columns(2)
    # Graphique dans la colonne 1: Tendance des additions à 12h
    with col1:
        st.markdown("### Tendance des additions à 12h")
        fig = px.line(
            df_report,
            x='Date',
            y='Additions 12h',
            color_discrete_sequence=[color_map_bar["Additions 12h"]]
        )
        fig.update_xaxes(tickformat="%d-%m-%y")
        st.plotly_chart(fig)
    # Graphique dans la colonne 2: Tendance des additions à 19h
    with col2:
        st.markdown("### Tendance des additions à 19h")
        fig = px.line(
            df_report,
            x='Date',
            y='Additions 19h',
            color_discrete_sequence=[color_map_bar["Additions 19h"]]
        )
        fig.update_xaxes(tickformat="%d-%m-%y")
        st.plotly_chart(fig)


    st.markdown("<hr/>", unsafe_allow_html=True)

    # 3. Analyse du panier moyen
    st.title("3. Analyse du panier moyen")

    # Création des colonnes
    col1, col2 = st.columns(2)
    # Graphique dans la colonne 1: Tendance du panier moyen à 12h
    with col1:
        st.markdown("### Tendance du panier moyen à 12h")
        fig = px.line(
            df_report,
            x='Date',
            y='Panier moyen 12h',
            color_discrete_sequence=[color_map_bar["Panier moyen 12h"]]
        )
        fig.update_xaxes(tickformat="%d-%m-%y")
        st.plotly_chart(fig)

    # Graphique dans la colonne 2: Tendance du panier moyen à 19h
    with col2:
        st.markdown("### Tendance du panier moyen à 19h")
        fig = px.line(
            df_report,
            x='Date',
            y='Panier moyen 19h',
            color_discrete_sequence=[color_map_bar["Panier moyen 19h"]]
        )
        fig.update_xaxes(tickformat="%d-%m-%y")
        st.plotly_chart(fig)


    st.markdown("<hr/>", unsafe_allow_html=True)

    # 4. Analyse du nbr de serveurs
    st.title("4. Analyse du nbr de serveurs")

    # Création des colonnes
    col1, col2 = st.columns(2)
    # Graphique dans la colonne 1: Total des additions
    with col1:
        st.markdown("### Total nbr serveurs")
        fig = px.bar(
            df_report.groupby('Jour')[['Nbr serveurs 12h','Nbr serveurs 19h']].sum().reset_index(),
            x='Jour',
            y=['Nbr serveurs 12h','Nbr serveurs 19h'],
            color_discrete_map=color_map_bar
        )
        st.plotly_chart(fig)

    # Création des colonnes
    col1, col2 = st.columns(2)
    # Graphique dans la colonne 1: Tendance du nbr de serveur à 12h
    with col1:
        st.markdown("### Tendance du nbr de serveur à 12h")
        fig = px.line(
            df_report,
            x='Date',
            y='Nbr serveurs 12h',
            color_discrete_sequence=[color_map_bar["Nbr serveurs 12h"]]
        )
        fig.update_xaxes(tickformat="%d-%m-%y")
        st.plotly_chart(fig)

    # Graphique dans la colonne 2: Tendance du nbr de serveur à 19h
    with col2:
        st.markdown("### Tendance du nbr de serveur à 19h")
        fig = px.line(
            df_report,
            x='Date',
            y='Nbr serveurs 19h',
            color_discrete_sequence=[color_map_bar["Nbr serveurs 19h"]]
        )
        fig.update_xaxes(tickformat="%d-%m-%y")
        st.plotly_chart(fig)


    st.markdown("<hr/>", unsafe_allow_html=True)

    # 5. Analyse de la météo
    st.title("5. Analyse de la météo")

    # Création des colonnes
    col1, col2 = st.columns(2)

    # Filtrage des données pour exclure les rangées où 'Météo 12h' est 'Inconnu'
    filtered_df_report_12 = df_report[df_report['Météo 12h'] != 'Inconnu']

    # Graphique dans la colonne 1: Influence de la météo sur le nombre de couverts à 12h
    with col1:
        st.markdown("### Influence de la météo sur le nbr de couverts à 12h")
        fig = px.bar(
            filtered_df_report_12.groupby('Météo 12h', observed=True)['Nbr total couv. 12h'].sum().reset_index(),
            x='Météo 12h',
            y='Nbr total couv. 12h',
            color_discrete_sequence=[color_map_bar["Nbr total couv. 12h"]]
        )
        st.plotly_chart(fig)

    df_report['Méteo 19h'] = df_report['Méteo 19h'].astype(str)
    filtered_df_report_19 = df_report[df_report['Méteo 19h'] != 'Inconnu']

    # Graphique dans la colonne 2: Influence de la météo sur le nombre de couverts à 19h
    with col2:
        st.markdown("### Influence de la météo sur le nbr de couverts à 19h")
        fig = px.bar(
            filtered_df_report_19.groupby('Méteo 19h')['Nbr total couv. 19h'].sum().reset_index(),
            x='Méteo 19h',
            y='Nbr total couv. 19h',
            color_discrete_sequence=[color_map_bar["Nbr total couv. 19h"]]
        )
        st.plotly_chart(fig)

    # Graphique dans la colonne 1: Influence de la température sur le nombre de couverts à 12h
    with col1:
        st.markdown("### Influence de la température sur le nbr de couverts à 12h")
        fig = px.bar(
            df_report.groupby('Temp. 12h')['Nbr total couv. 12h'].sum().reset_index(),
            x='Temp. 12h',
            y='Nbr total couv. 12h',
            color_discrete_sequence=[color_map_bar["Nbr total couv. 12h"]]
        )
        st.plotly_chart(fig)

    # Graphique dans la colonne 2: Influence de la température sur le nombre de couverts à 19h
    with col2:
        st.markdown("### Influence de la température sur le nbr de couverts à 19h")
        fig = px.bar(
            df_report.groupby('Temp. 19h')['Nbr total couv. 19h'].sum().reset_index(),
            x='Temp. 19h',
            y='Nbr total couv. 19h',
            color_discrete_sequence=[color_map_bar["Nbr total couv. 19h"]]
        )
        st.plotly_chart(fig)

    st.markdown("<hr/>", unsafe_allow_html=True)


    footer.display()



    st.markdown("<hr/>", unsafe_allow_html=True)


    return filtered_df





if __name__ == "__main__":
    print(main().columns)
