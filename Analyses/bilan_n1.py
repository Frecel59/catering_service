# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd


def analyses_bilan_n1 (jours_moments_selectionnes_a, filtered_a, filtered_a2):
    def calculate_total(row, column_name):
        jour_a = row['Jour']
        moments_selectionnes = jours_moments_selectionnes_a[jour_a]
        total = 0
        if 'Midi' in moments_selectionnes:
            total += row[f'{column_name} 12h']
        if 'Soir' in moments_selectionnes:
            total += row[f'{column_name} 19h']
        return total

    columns = {
        'Nbr total couv.': 'Nbr total couv.',
        'Additions': 'Total_CA_Selected',
        'Nbr couv. off': 'Nbr couv. offerts',
        'Additions off': 'Total_CA_Offerts_Selected'
    }

    for df in [filtered_a, filtered_a2]:
        for old_col, new_col in columns.items():
            df[new_col] = df.apply(lambda row: calculate_total(row, old_col), axis=1)

    cols_to_analyze = [
        'Nbr total couv.', 'Total_CA_Selected',
        'Nbr couv. offerts', 'Total_CA_Offerts_Selected'
    ]

    results = []
    for col in cols_to_analyze:
        total_n = filtered_a[col].sum()
        total_n1 = filtered_a2[col].sum()
        mean_n = filtered_a[col].mean()
        mean_n1 = filtered_a2[col].mean()
        total_variation = ((total_n - total_n1) / total_n1) * 100 if total_n1 != 0 else 0
        column_mapping = {
            'Nbr total couv.': 'Nbr total couv.',
            'Total_CA_Selected': 'Total Additions',
            'Nbr couv. offerts': 'Nbr couv. offerts',
            'Total_CA_Offerts_Selected': 'Total offerts'
        }
        results.append({
            'Indicateur': column_mapping[col],
            'Total N': total_n,
            'Total N-1': total_n1,
            'Variation (%)': total_variation,
            'Moyenne N': mean_n,
            'Moyenne N-1': mean_n1,
        })

    # Panier Moyen calculation after 'Total Additions' row is appended
    panier_moyen = {
        'Indicateur': 'Panier Moyen',
        'Total N': results[1]['Total N'] / results[0]['Total N'] if results[0]['Total N'] != 0 else 0,
        'Total N-1': results[1]['Total N-1'] / results[0]['Total N-1'] if results[0]['Total N-1'] != 0 else 0,
        'Variation (%)': 0,  # You may need to calculate this manually
        'Moyenne N': "-",
        'Moyenne N-1': "-",
    }
    # Variation calculation for Panier Moyen
    panier_moyen['Variation (%)'] = ((panier_moyen['Total N'] - panier_moyen['Total N-1']) / panier_moyen['Total N-1']) * 100 if panier_moyen['Total N-1'] != 0 else 0

    # Insert Panier Moyen row at the desired position
    results.insert(2, panier_moyen)  # Adjust the index 2 to the desired position

    result_df_n1 = pd.DataFrame(results)
    result_df1_n1 = result_df_n1.set_index('Indicateur')

    # Appliquer le formatage ici
    def format_numbers(value):
        if isinstance(value, (int, float)):
            if value.is_integer():
                return f"{value:,.0f}".replace(",", " ")
            else:
                return f"{value:,.2f}".replace(",", " ").replace(".", ",")
        else:
            return value

    def format_percent(value):
        if isinstance(value, (int, float)):
            return f"{value:,.2f}%".replace(",", " ").replace(".", ",")
        else:
            return value

    # Appliquer les fonctions de formatage
    result_df1_n1[['Total N', 'Total N-1', 'Moyenne N', 'Moyenne N-1']] = result_df1_n1[['Total N', 'Total N-1', 'Moyenne N', 'Moyenne N-1']].applymap(format_numbers)
    result_df1_n1['Variation (%)'] = result_df1_n1['Variation (%)'].apply(format_percent)



    return result_df_n1, result_df1_n1
