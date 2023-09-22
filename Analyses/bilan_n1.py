# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd


def analyses_bilan_n1 (jours_moments_selectionnes_a, filtered_a, filtered_a2):
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

    # Liste des colonnes d'origine et des nouvelles colonnes pour les totaux
    columns = {
        'Nbr total couv.': 'Nbr total couv.',
        'Nbr couv. off': 'Nbr couv. offerts',
        'Additions': 'Total_CA_Selected',
        'Additions off': 'Total_CA_Offerts_Selected'
    }

    # Boucle sur les DataFrames et les colonnes
    for df in [filtered_a, filtered_a2]:
        for old_col, new_col in columns.items():
            df[new_col] = df.apply(lambda row: calculate_total(row, old_col), axis=1)


    # 1. Identifier les colonnes pertinentes à analyser
    cols_to_analyze = [
        'Nbr total couv.', 'Nbr couv. offerts',
        'Total_CA_Selected', 'Total_CA_Offerts_Selected'

    ]

    # 2. Calculer les totaux et les moyennes
    results = []
    for col in cols_to_analyze:
        total_n = filtered_a[col].sum()
        total_n1 = filtered_a2[col].sum()

        mean_n = filtered_a[col].mean()
        mean_n1 = filtered_a2[col].mean()

        # 3. Calculer le pourcentage de variation
        total_variation = ((total_n - total_n1) / total_n1) * 100 if total_n1 != 0 else 0
        mean_variation = ((mean_n - mean_n1) / mean_n1) * 100 if mean_n1 != 0 else 0

        results.append({
            'Indicateur': col,
            'Total N': total_n,
            'Total N-1': total_n1,
            'Variation Total (%)': total_variation,
            'Moyenne N': mean_n,
            'Moyenne N-1': mean_n1,
            'Variation Moyenne (%)': mean_variation
        })

    # 4. Créer un dataframe pour afficher ces résultats
    result_df_n1 = pd.DataFrame(results)

    # # Supprimer l'index par défaut du DataFrame
    # result_df1_n1 = result_df_n1.set_index('Types')

    # # Formater les colonnes du DataFrame
    # result_df1_n1['Nbr Couverts'] = result_df1_n1['Nbr Couverts'].apply\
    #     (lambda x: f"{x:,}".replace(",", " "))
    # result_df1_n1['%'] = result_df1_n1['%'].apply(lambda x: f"{x:.2f}")
    # result_df1_n1['Total Additions €'] = result_df1_n1['Total Additions €'].apply\
    #     (lambda x: f"{x:,.2f}".replace(",", " "))
    # result_df1_n1['Panier moyen €'] = result_df1_n1['Panier moyen €'].apply\
    #     (lambda x: f"{x:.2f}")

    return result_df_n1
