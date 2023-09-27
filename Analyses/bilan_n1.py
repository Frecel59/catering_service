# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd


def analyses_bilan_n1(jours_moments_selectionnes_a, filtered_a, filtered_a2):
    # Créer une fonction générique pour calculer les totaux en fonction du
    # jour et du moment sélectionnés
    def calculate_total(row, column_name):
        jour_a = row['Jour']
        moments_selectionnes = jours_moments_selectionnes_a[jour_a]

        total = 0
        if 'Midi' in moments_selectionnes:
            total += row[f'{column_name} 12h']
        if 'Soir' in moments_selectionnes:
            total += row[f'{column_name} 19h']

        return total

    def calculate_totals(df, jours_moments_selectionnes):
        result = {
            'Payants': {
                'Nbr Couverts 12h': df.apply(calculate_total, args=('Nbr couv', jours_moments_selectionnes), axis=1).sum(),
                'Nbr Couverts 19h': df.apply(calculate_total, args=('Nbr couv', jours_moments_selectionnes), axis=1).sum(),
                'Total Additions €': df.apply(calculate_total, args=('Additions', jours_moments_selectionnes), axis=1).sum(),
            },
            'Offerts': {
                'Nbr Couverts 12h': df.apply(calculate_total, args=('Nbr couv. off', jours_moments_selectionnes), axis=1).sum(),
                'Nbr Couverts 19h': df.apply(calculate_total, args=('Nbr couv. off', jours_moments_selectionnes), axis=1).sum(),
                'Total Additions €': df.apply(calculate_total, args=('Additions off', jours_moments_selectionnes), axis=1).sum(),
            }
        }


        # Calculs pour la ligne "Total"
        result['Total'] = {
            'Nbr Couverts 12h': result['Payants']['Nbr Couverts 12h'] + result['Offerts']['Nbr Couverts 12h'],
            'Nbr Couverts 19h': result['Payants']['Nbr Couverts 19h'] + result['Offerts']['Nbr Couverts 19h'],
            'Total Additions €': result['Payants']['Total Additions €'] + result['Offerts']['Total Additions €'],
        }

        # Calculs des colonnes additionnelles
        for key in result:
            result[key]['Nbr Couverts Total'] = result[key]['Nbr Couverts 12h'] + result[key]['Nbr Couverts 19h']
            result[key]['Panier moyen €'] = result[key]['Total Additions €'] / result[key]['Nbr Couverts Total'] if result[key]['Nbr Couverts Total'] != 0 else 0
            result[key]['%'] = 100 * result[key]['Nbr Couverts Total'] / result['Total']['Nbr Couverts Total'] if result['Total']['Nbr Couverts Total'] != 0 else 0

        # Conversion en DataFrame
        result_df_n1 = pd.DataFrame(result).transpose()

        # Supprimer l'index par défaut du DataFrame
        result_df1_n1 = result_df_n1.set_index('Indicateur')

        return result_df_n1, result_df1_n1

    # Appeler la fonction calculate_totals pour chaque DataFrame et retourner les résultats
    return calculate_totals(filtered_a, jours_moments_selectionnes_a), calculate_totals(filtered_a2, jours_moments_selectionnes_a)
