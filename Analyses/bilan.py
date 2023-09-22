# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd


def analyses_bilan (jours_moments_selectionnes, filtered_vsd):
    # Créer une fonction générique pour calculer les totaux en fonction du
    # jour et du moment sélectionnés
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
    filtered_vsd['Total_Couv_Selected'] = filtered_vsd.apply(lambda row: \
        calculate_total(row, 'Nbr total couv.'), axis=1)

    # Utiliser la fonction pour calculer le total de couverts offerts
    filtered_vsd['Total_Couv_Off_Selected'] = filtered_vsd.apply(lambda row: \
        calculate_total(row, 'Nbr couv. off'), axis=1)

    # Utiliser la fonction pour calculer le total CA
    filtered_vsd['Total_CA_Selected'] = filtered_vsd.apply(lambda row: \
        calculate_total(row, 'Additions'), axis=1)

    # Utiliser la fonction pour calculer le total CA
    filtered_vsd['Total_CA_Offerts_Selected'] = filtered_vsd.apply(lambda row: \
        calculate_total(row, 'Additions off'), axis=1)


    # Calculer la somme des couverts pour les jours et moments sélectionnés
    total_couv_selected = filtered_vsd['Total_Couv_Selected'].sum()


    # Calculer la somme des couverts offerts pour les jours et moments sélectionnés
    total_couv_off_selected = filtered_vsd['Total_Couv_Off_Selected'].sum()


     # Calculer la somme des couverts payants pour les jours et moments sélectionnés
    total_couv_payant_selected = total_couv_selected - total_couv_off_selected


    # Calculer le % des couverts offerts par rapport au total des couverts
    if total_couv_selected != 0:
        percent_total_couv_off_selected = (total_couv_off_selected \
            / total_couv_selected) * 100

    else:
        percent_total_couv_off_selected = 0


    # Calculer le % des couverts payant par rapport au total des couverts
    percent_total_couv_payant_selected = ((total_couv_selected - \
        total_couv_off_selected) / total_couv_selected) * 100

    # Calculer le CA pour les jours et moments sélectionnés
    total_ca_selected = filtered_vsd['Total_CA_Selected'].sum()

    # Calculer les offerts pour les jours et moments sélectionnés
    total_ca_offerts_selected = filtered_vsd['Total_CA_Offerts_Selected'].sum()

    # Calculer panier moyen total pour les jours et moments sélectionnés
    if total_couv_selected != 0:
        panier_moyen_selected = total_ca_selected / total_couv_selected

    else:
        total_couv_selected = 0
        panier_moyen_selected = '-'

    # Calculer panier moyen des payants pour les jours et moments sélectionnés
    if total_couv_payant_selected != 0:
        panier_moyen_payants_selected = total_ca_selected \
            / total_couv_payant_selected

    else:
        total_couv_payant_selected = 0
        panier_moyen_payants_selected = '-'

    # Calculer panier moyen des offerts pour les jours et moments sélectionnés
    if total_couv_off_selected != 0:
        panier_moyen_off_selected = total_ca_offerts_selected \
            / total_couv_off_selected

    else:
        total_couv_off_selected = 0
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
    result_df1['Nbr Couverts'] = result_df1['Nbr Couverts'].apply\
        (lambda x: f"{x:,}".replace(",", " "))
    result_df1['%'] = result_df1['%'].apply(lambda x: f"{x:.2f}")
    result_df1['Total Additions €'] = result_df1['Total Additions €'].apply\
        (lambda x: f"{x:,.2f}".replace(",", " "))
    result_df1['Panier moyen €'] = result_df1['Panier moyen €'].apply\
        (lambda x: f"{x:.2f}")

    return result_df, result_df1
