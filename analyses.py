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
    ###################### CALCUL SUR LE DATAFRAME ##########################
    #########################################################################

    columns_to_sum = ['Nbr couv. 19h', 'Additions 19h', 'Nbr couv. off 19h', 'Additions off 19h', 'Nbr couv 12h', 'Additions 12h', 'Nbr couv. off 12h', 'Additions off 12h']
    sums = filtered_df[columns_to_sum].sum()

    # Sommes des covers et des prices
    total_Covers_sales = sums['Nbr couv. 19h'] + sums['Nbr couv 12h']
    total_Price_sales = sums['Additions 19h'] + sums['Additions 12h']
    total_Covers_intern = sums['Nbr couv. off 19h'] + sums['Nbr couv. off 12h']
    total_Price_intern = sums['Additions off 19h'] + sums['Additions off 12h']
    total_Covers = total_Covers_sales + total_Covers_intern

    # Pourcentage des covers et des prices
    percentage_Covers_sales = (total_Covers_sales / total_Covers) * 100
    percentage_Covers_intern = (total_Covers_intern / total_Covers) * 100

    # Panier moyen
    panier_sales = total_Price_sales / total_Covers_sales
    panier_intern = total_Price_intern / total_Covers_intern
    panier_total = total_Price_sales / total_Covers

    # Créer une liste de tuples pour chaque ligne du tableau
    # Formater les valeurs dans la colonne "Nbr Couverts" sans décimales et avec un espace comme séparateur de milliers
    total_Covers_sales_formatted = f"{int(total_Covers_sales):,}".replace(",", " ")
    total_Covers_intern_formatted = f"{int(total_Covers_intern):,}".replace(",", " ")
    total_Covers_formatted = f"{int(total_Covers):,}".replace(",", " ")

    table_data_global = [
        ("Payants", total_Covers_sales_formatted, f"{percentage_Covers_sales:.2f} %", f"{total_Price_sales:,.2f} €", f"{panier_sales:,.2f} €"),
        ("Offerts", total_Covers_intern_formatted, f"{percentage_Covers_intern:.2f}%", f"{total_Price_intern:,.2f} €", f"{panier_intern:,.2f} €"),
        ("Réalisés", total_Covers_formatted, "100 %", f"{total_Price_sales:,.2f} €", f"{panier_total:,.2f} €"),
    ]

    #########################################################################
    ###################### AFFICHAGE DU BILAN ###############################
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

    formatted_table = tabulate(table_data_global, headers=["Type", "Nbr Couverts", "%", "Total", "Panier moyen"], tablefmt="fancy_grid")
    st.text(formatted_table)

    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    #########################################################################
    ################# AFFICHAGE DU BILAN VEND SOIR AU DIM SOIR ##############
    #########################################################################

    # Liste des jours de la semaine
    jours_semaine = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

    # Créez un dictionnaire pour stocker les moments sélectionnés pour chaque jour
    jours_moments_selectionnes = {}

    # Initialiser select_all à True pour tout cocher par défaut
    select_all = True

    # Utilisez un expander pour afficher les cases à cocher
    with st.expander("Sélectionnez les jours et services"):
        # Ajoutez une case à cocher pour tout cocher/décocher
        select_all = st.checkbox("Tout cocher/décocher", key="select_all", value=select_all)


        for jour in jours_semaine:
            jours_moments_selectionnes[jour] = []
            if select_all:  # Si "Tout cocher/décocher" est coché, cochez automatiquement les cases individuelles
                midi = st.checkbox(f'{jour} - Midi', key=f'{jour}_midi', value=True)
                soir = st.checkbox(f'{jour} - Soir', key=f'{jour}_soir', value=True)
            else:
                midi = st.checkbox(f'{jour} - Midi', key=f'{jour}_midi')
                soir = st.checkbox(f'{jour} - Soir', key=f'{jour}_soir')

            # Si la case "Midi" est cochée, ajoutez "Midi" à la liste des moments sélectionnés pour ce jour
            if midi:
                jours_moments_selectionnes[jour].append("Midi")

            # Si la case "Soir" est cochée, ajoutez "Soir" à la liste des moments sélectionnés pour ce jour
            if soir:
                jours_moments_selectionnes[jour].append("Soir")

    # Filtrer les données en fonction des jours sélectionnés
    filtered_vsd = filtered_df[filtered_df['Jour'].isin([jour for jour, _ in jours_moments_selectionnes.items()])]

    # # Créer une colonne pour le total de couverts en fonction du jour et du moment sélectionnés
    # def calculate_total_couv(row):
    #     jour = row['Jour']
    #     moments_selectionnes = jours_moments_selectionnes[jour]

    #     total_couv = 0
    #     if 'Midi' in moments_selectionnes:
    #         total_couv += row['Nbr total couv. 12h']
    #     if 'Soir' in moments_selectionnes:
    #         total_couv += row['Nbr total couv. 19h']

    #     return total_couv

    # # Créer une colonne pour le total de couverts offerts en fonction du jour et du moment sélectionnés
    # def calculate_total_couv_off(row):
    #     jour = row['Jour']
    #     moments_selectionnes = jours_moments_selectionnes[jour]

    #     total_couv_off = 0
    #     if 'Midi' in moments_selectionnes:
    #         total_couv_off += row['Nbr couv. off 12h']
    #     if 'Soir' in moments_selectionnes:
    #         total_couv_off += row['Nbr couv. off 19h']

    #     return total_couv_off

    # # Créer une colonne pour le total CA en fonction du jour et du moment sélectionnés
    # def calculate_total_ca(row):
    #     jour = row['Jour']
    #     moments_selectionnes = jours_moments_selectionnes[jour]

    #     total_ca = 0
    #     if 'Midi' in moments_selectionnes:
    #         total_ca += row['Additions 12h']
    #     if 'Soir' in moments_selectionnes:
    #         total_ca += row['Additions 19h']

    #     return total_ca


    # filtered_vsd['Total_Couv_Selected'] = filtered_vsd.apply(calculate_total_couv, axis=1)
    # filtered_vsd['Total_Couv_Off_Selected'] = filtered_vsd.apply(calculate_total_couv_off, axis=1)
    # filtered_vsd['Total_CA_Selected'] = filtered_vsd.apply(calculate_total_ca, axis=1)

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


    # Calculer la somme des couverts pour les jours et moments sélectionnés
    total_couv_selected = filtered_vsd['Total_Couv_Selected'].sum()
    total_couv_selected_formatted = f"{int(total_couv_selected):,}".replace(",", " ")

    # Calculer la somme des couverts offerts pour les jours et moments sélectionnés
    total_couv_off_selected = filtered_vsd['Total_Couv_Off_Selected'].sum()
    total_couv_off_selected_formatted = f"{int(total_couv_off_selected):,}".replace(",", " ")

    # Calculer le pourcentage des couverts offerts par rapport au total des couverts
    if total_couv_selected != 0:
        percent_total_couv_off_selected = (total_couv_off_selected / total_couv_selected) * 100
        percent_total_couv_off_selected_formatted = f"{int(percent_total_couv_off_selected):,}".replace(",", " ")
    else:
        percent_total_couv_off_selected = 0  # Si total_couv_selected est égal à zéro, le pourcentage est défini à zéro
        percent_total_couv_off_selected_formatted = percent_total_couv_off_selected

    # Calculer le CA pour les jours et moments sélectionnés
    total_ca_selected = filtered_vsd['Total_CA_Selected'].sum()
    total_ca_selected_formatted = f"{int(total_ca_selected):,}".replace(",", " ")

    # Calculer panier moyen pour les jours et moments sélectionnés
    if total_couv_selected != 0:
        panier_moyen_selected = total_ca_selected / total_couv_selected
        panier_moyen_selected_formatted = f"{int(panier_moyen_selected):,}".replace(",", " ")
    else:
        total_couv_selected = 0  # Si total_couv_selected est égal à zéro, le résultat n'est pas affiché
        panier_moyen_selected_formatted = '-'

    st.text(f"Nbr de couverts total : {total_couv_selected_formatted}")
    st.text(f"Nbr de couverts offerts : {total_couv_off_selected_formatted} ({percent_total_couv_off_selected_formatted} %)")
    st.text(f"CA : {total_ca_selected_formatted} €")
    st.text(f"Panier moyen : {panier_moyen_selected_formatted} €")

    # Créer un dictionnaire avec les résultats et les noms de colonnes
    result_data = {
        "Types": ["Nbr de couverts total", "Nbr de couverts offerts", "CA", "Panier moyen"],
        "Résultats": [
            total_couv_selected_formatted,
            f"{total_couv_off_selected_formatted} ({percent_total_couv_off_selected_formatted} %)",
            total_ca_selected_formatted + " €",
            panier_moyen_selected_formatted + " €"
        ]
    }

    # Créer un DataFrame à partir du dictionnaire
    result_df = pd.DataFrame(result_data)

    # Supprimer l'index par défaut du DataFrame
    result_df1 = result_df.set_index('Types')

    # Afficher le DataFrame dans un tableau
    st.dataframe(result_df1)

    # Créer un objet BytesIO pour stocker les données Excel
    output = io.BytesIO()

    # Utiliser Pandas pour sauvegarder le DataFrame au format Excel dans l'objet BytesIO
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        result_df.to_excel(writer, sheet_name='Sheet1', index=False)

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
