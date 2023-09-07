import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from tabulate import tabulate
import io
import matplotlib.pyplot as plt

from Data_cleaning.Clean_data import clean_file_in_folder
from Data_cleaning.Clean_data_snack import clean_file_in_folder_snack
from Data_cleaning.df_global import merged_df
from Analyses.graph import show_grouped_data






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

    st.title("Analyses")


    brasserie_start = clean_file_in_folder().Date.min().strftime("%d/%m/%Y")
    brasserie_end = clean_file_in_folder().Date.max().strftime("%d/%m/%Y")
    snack_start = clean_file_in_folder_snack().Date.min().strftime("%d/%m/%Y")
    snack_end = clean_file_in_folder_snack().Date.max().strftime("%d/%m/%Y")

    st.write("")
    formatted_period_brasserie = f"Brasserie données disponibles : du {brasserie_start} au {brasserie_end}"
    formatted_period_snack = f"Snack données disponibles : du {snack_start} au {snack_end}"
    st.markdown(f'<p class="period-text">{formatted_period_brasserie}</br>{formatted_period_snack}</p>', unsafe_allow_html=True)

    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    #########################################################################
    ############# CHAMPS INPUT POUR LE CHOIX DE LA PERIODE ##################
    #########################################################################

    # Appeler la fonction merged_df pour obtenir les données avec météo
    df_final = merged_df()

    st.markdown(f'<p class="period-text">Choississez une période</p>', unsafe_allow_html=True)

    # Créer une mise en page en colonnes
    col1, col2 = st.columns(2)

    # Ajouter le widget date_input dans la première colonne
    with col1:
        start_date = st.date_input("Date de départ", datetime((df_final["Date"].max()).year - 1, 11, 1), key="start_date_input", format="DD/MM/YYYY") # 01/11 + année -1 de date max
        formatted_start_date = format_date_in_french(start_date)

    with col2:
        end_date = st.date_input("Date de fin", df_final["Date"].max(), key="end_date_input", format="DD/MM/YYYY")
        formatted_end_date = format_date_in_french(end_date)

    # Convertir les dates sélectionnées en objets datetime64[ns]
    start_date_convert = pd.to_datetime(start_date)
    end_date_convert = pd.to_datetime(end_date)

    # Filtrer le DataFrame en fonction des dates choisies
    filtered_df = df_final[(df_final["Date"] >= start_date_convert) & (df_final["Date"] <= end_date_convert)]


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
    formatted_period = f"Bilan de la période : du {formatted_start_date} au {formatted_end_date}"
    st.markdown(f'<p class="period-text2">{formatted_period}</p>', unsafe_allow_html=True)



    # Liste des jours de la semaine
    jours_semaine = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

    # Créez un dictionnaire pour stocker les moments sélectionnés pour chaque jour
    jours_moments_selectionnes = {}

    # Utilisez un expander pour afficher les cases à cocher
    with st.expander("Sélectionnez les jours et services"):
        for jour in jours_semaine:
            jours_moments_selectionnes[jour] = []

            # Les cases sont cochées par défaut
            midi = st.checkbox(f'{jour} - Midi', key=f'{jour}_midi', value=True)
            soir = st.checkbox(f'{jour} - Soir', key=f'{jour}_soir', value=True)

            # Si la case "Midi" est cochée, ajoutez "Midi" à la liste des moments sélectionnés pour ce jour
            if midi:
                jours_moments_selectionnes[jour].append("Midi")

            # Si la case "Soir" est cochée, ajoutez "Soir" à la liste des moments sélectionnés pour ce jour
            if soir:
                jours_moments_selectionnes[jour].append("Soir")

    # Filtrer les données en fonction des jours sélectionnés
    filtered_vsd = filtered_df[filtered_df['Jour'].isin([jour for jour, _ in jours_moments_selectionnes.items()])]



    # Créer une fonction générique pour calculer les totaux en fonction du jour et du moment sélectionnés
    def calculate_total(row, column_name):
        jour = row['Jour']
        moments_selectionnes = jours_moments_selectionnes[jour]

        total = 0
        if 'Midi' in moments_selectionnes:
            total += row[f'{column_name} 12h']
        if 'Soir' in moments_selectionnes:
            total += row[f'{column_name} 19h']

        return total

    # Utiliser la fonction pour calculer le total de couverts
    filtered_vsd['Total_Couv_Selected'] = filtered_vsd.apply(lambda row: calculate_total(row, 'Nbr total couv.'), axis=1)

    # Utiliser la fonction pour calculer le total de couverts offerts
    filtered_vsd['Total_Couv_Off_Selected'] = filtered_vsd.apply(lambda row: calculate_total(row, 'Nbr couv. off'), axis=1)

    # Utiliser la fonction pour calculer le total CA
    filtered_vsd['Total_CA_Selected'] = filtered_vsd.apply(lambda row: calculate_total(row, 'Additions'), axis=1)

    # Utiliser la fonction pour calculer le total CA
    filtered_vsd['Total_CA_Offerts_Selected'] = filtered_vsd.apply(lambda row: calculate_total(row, 'Additions off'), axis=1)


    # Calculer la somme des couverts pour les jours et moments sélectionnés
    total_couv_selected = filtered_vsd['Total_Couv_Selected'].sum()


    # Calculer la somme des couverts offerts pour les jours et moments sélectionnés
    total_couv_off_selected = filtered_vsd['Total_Couv_Off_Selected'].sum()


     # Calculer la somme des couverts payants pour les jours et moments sélectionnés
    total_couv_payant_selected = total_couv_selected - total_couv_off_selected


    # Calculer le % des couverts offerts par rapport au total des couverts
    if total_couv_selected != 0:
        percent_total_couv_off_selected = (total_couv_off_selected / total_couv_selected) * 100

    else:
        percent_total_couv_off_selected = 0  # Si total_couv_selected est égal à zéro, le pourcentage est défini à zéro


    # Calculer le % des couverts payant par rapport au total des couverts
    percent_total_couv_payant_selected = ((total_couv_selected - total_couv_off_selected) / total_couv_selected) * 100

    # Calculer le CA pour les jours et moments sélectionnés
    total_ca_selected = filtered_vsd['Total_CA_Selected'].sum()

    # Calculer les offerts pour les jours et moments sélectionnés
    total_ca_offerts_selected = filtered_vsd['Total_CA_Offerts_Selected'].sum()

    # Calculer panier moyen total pour les jours et moments sélectionnés
    if total_couv_selected != 0:
        panier_moyen_selected = total_ca_selected / total_couv_selected

    else:
        total_couv_selected = 0  # Si total_couv_selected est égal à zéro, le résultat n'est pas affiché
        panier_moyen_selected = '-'

    # Calculer panier moyen des payants pour les jours et moments sélectionnés
    if total_couv_payant_selected != 0:
        panier_moyen_payants_selected = total_ca_selected / total_couv_payant_selected

    else:
        total_couv_payant_selected = 0  # Si total_couv_selected est égal à zéro, le résultat n'est pas affiché
        panier_moyen_payants_selected = '-'

    # Calculer panier moyen des offerts pour les jours et moments sélectionnés
    if total_couv_off_selected != 0:
        panier_moyen_off_selected = total_ca_offerts_selected / total_couv_off_selected

    else:
        total_couv_off_selected = 0  # Si total_couv_selected est égal à zéro, le résultat n'est pas affiché
        panier_moyen_off_selected = '-'


    # Créer un dictionnaire avec les résultats et les noms de colonnes
    result_data = {
        "Types": ["Payants", "Offerts", "Total"],
        "Nbr Couverts": [
            total_couv_payant_selected,
            total_couv_off_selected,
            total_couv_selected,
        ],
        "%": [
            percent_total_couv_payant_selected,
            percent_total_couv_off_selected,
            100.0,
        ],
        "Total Additions €": [
            total_ca_selected,
            total_ca_offerts_selected,
            total_ca_selected,
        ],
        "Panier moyen €": [
            panier_moyen_payants_selected,
            panier_moyen_off_selected,
            panier_moyen_selected,
        ],
    }

    # Créer un DataFrame à partir du dictionnaire
    result_df = pd.DataFrame(result_data)

    # Supprimer l'index par défaut du DataFrame
    result_df1 = result_df.set_index('Types')

    # Formater les colonnes du DataFrame
    result_df1['Nbr Couverts'] = result_df1['Nbr Couverts'].apply(lambda x: f"{x:,}".replace(",", " "))
    result_df1['%'] = result_df1['%'].apply(lambda x: f"{x:.2f}")
    result_df1['Total Additions €'] = result_df1['Total Additions €'].apply(lambda x: f"{x:,.2f}".replace(",", " "))
    result_df1['Panier moyen €'] = result_df1['Panier moyen €'].apply(lambda x: f"{x:.2f}")

    # Afficher le DataFrame en occupant toute la largeur de la page
    st.table(result_df1)


    # Créer un objet BytesIO pour stocker les données Excel
    output = io.BytesIO()

    # Multipliez la colonne % par 100 pour obtenir la représentation en pourcentage correcte
    result_df['%'] /= 100

    # Utiliser Pandas pour sauvegarder le DataFrame au format Excel dans l'objet BytesIO
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        result_df.to_excel(writer, sheet_name='Sheet1', index=False)

        # Accédez à la feuille Excel générée pour formater les colonnes
        worksheet = writer.sheets['Sheet1']

        # Créez un format pour les nombres avec séparateur de milliers
        number_format = writer.book.add_format({'num_format': '#,##0'})

        # Créer un format comptabilité avec 2 décimales
        compte_format = writer.book.add_format({'num_format': '#,##0.00 €'})

        # Créer un format pourcentage avec 2 décimales
        percent_format = writer.book.add_format({'num_format': '0.00%'})

        # # Créez un format de nombre avec deux décimales
        # number_format_2_decimal = writer.book.add_format({'num_format': '0.00'})

        # Appliquer le format correspondant
        worksheet.set_column('B:B', None, number_format)  # Colonne 'Nbr Couverts'
        worksheet.set_column('C:C', None, percent_format)  # Colonne '%'
        worksheet.set_column('D:D', None, compte_format)  # Colonne 'Total Additions €'
        worksheet.set_column('E:E', None, compte_format)  # Colonne 'Panier moyen €'

    # Définir le point de départ pour la lecture
    output.seek(0)

    # Utilisez st.download_button pour afficher un bouton de téléchargement
    st.download_button(
        label=f"Télécharger au format Excel",  # Utilisez la date dans le nom du fichier
        data=output,
        file_name=f"bilan_{formatted_start_date}_{formatted_end_date}.xlsx",  # Spécifiez ici le nom du fichier Excel avec la date
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

    # Créer les widgets
    # Créer une mise en page en colonnes
    col1, col2, col3 = st.columns(3)

    # Ajouter le widget date_input dans la première colonne
    with col1:
        group_by_option = st.selectbox('Trier par :', ['Jour', 'Mois et Jour'])

    with col2:
        data_type_option = st.selectbox('Type de données :', ['Nbr total couv. 12h', 'Nbr total couv. 19h', 'Nbr total couv.', 'Additions 12h', 'Additions 19h', 'Total additions'])


    if group_by_option == 'Mois et Jour':
        unique_months = graph_df['Date'].dt.to_period("M").unique().strftime('%m/%Y').tolist()
        with col3:
            month_option = st.selectbox('Mois :', unique_months)

    else:
        month_option = None

    # Afficher le graphique en fonction des widgets
    show_grouped_data(group_by_option, data_type_option, group_by_option, data_type_option, month_option, graph_df)

    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    ####################################################################
    ######### AFFICHAGE DU DATAFRAME AVEC POSSIBILITE DE FILTRE ########
    ####################################################################

    st.markdown(f'<p class="period-text">Données avec météo pour la période sélectionnée :</p>', unsafe_allow_html=True)

    # Convertissez les colonnes "Date" et "date" en datetime
    filtered_table = filtered_df.assign(Date=pd.to_datetime(filtered_df['Date']))


    # Formatez les colonnes "Date" et "date" pour les afficher au format "dd-mm-yyyy"
    filtered_table = filtered_table.assign(Date=filtered_table['Date'].dt.strftime("%d-%m-%Y"))


    # Ajoutez des cases à cocher pour permettre à l'utilisateur de sélectionner les colonnes à afficher
    selected_columns = st.multiselect(
        'Sélectionnez les colonnes à afficher',
        options=filtered_table.columns,
        default=filtered_table.columns.tolist()  # Pour afficher toutes les colonnes par défaut
    )

    # Filtrer le DataFrame en fonction des colonnes sélectionnées
    filtered_table = filtered_table[selected_columns]

    # Affichez le DataFrame filtré
    st.dataframe(filtered_table)


    # Créer un objet BytesIO pour stocker les données Excel
    output2 = io.BytesIO()

    # Utiliser Pandas pour sauvegarder le DataFrame au format Excel dans l'objet BytesIO
    with pd.ExcelWriter(output2, engine='xlsxwriter') as writer:
        filtered_table.to_excel(writer, sheet_name='Sheet1', index=False)

    # Définir le point de départ pour la lecture
    output2.seek(0)

    # Utilisez st.download_button pour afficher un bouton de téléchargement
    st.download_button(
        label=f"Télécharger au format Excel",  # Utilisez la date dans le nom du fichier
        data=output2,
        file_name=f"donnees_{formatted_start_date}_{formatted_end_date}.xlsx",  # Spécifiez ici le nom du fichier Excel avec la date
        key="download_results2"
        )



    return filtered_df





if __name__ == "__main__":
    print(main().columns)
