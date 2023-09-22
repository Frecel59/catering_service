import streamlit as st
import pandas as pd

def analyses_bilan(jours_moments_selectionnes, filtered_vsd):

    def calculate_total(row, column_name):
        return sum([row[f'{column_name} {time}'] for time in jours_moments_selectionnes[row['Jour']]])

    columns_to_calculate = {
        'Total_Couv_Selected': 'Nbr total couv.',
        'Total_Couv_Off_Selected': 'Nbr couv. off',
        'Total_CA_Selected': 'Additions',
        'Total_CA_Offerts_Selected': 'Additions off'
    }

    for new_col, old_col in columns_to_calculate.items():
        filtered_vsd[new_col] = filtered_vsd.apply(lambda row: calculate_total(row, old_col), axis=1)

    totals = {
        'total_couv_selected': filtered_vsd['Total_Couv_Selected'].sum(),
        'total_couv_off_selected': filtered_vsd['Total_Couv_Off_Selected'].sum(),
        'total_ca_selected': filtered_vsd['Total_CA_Selected'].sum(),
        'total_ca_offerts_selected': filtered_vsd['Total_CA_Offerts_Selected'].sum()
    }

    totals['total_couv_payant_selected'] = totals['total_couv_selected'] - totals['total_couv_off_selected']

    panier_moyen = {
        'total': totals['total_ca_selected'] / totals['total_couv_selected'] if totals['total_couv_selected'] else '-',
        'payants': totals['total_ca_selected'] / totals['total_couv_payant_selected'] if totals['total_couv_payant_selected'] else '-',
        'offerts': totals['total_ca_offerts_selected'] / totals['total_couv_off_selected'] if totals['total_couv_off_selected'] else '-'
    }

    result_data = {
        "Types": ["Payants", "Offerts", "Total"],
        "Nbr Couverts": [
            totals['total_couv_payant_selected'],
            totals['total_couv_off_selected'],
            totals['total_couv_selected'],
        ],
        "%": [
            100.0 * totals['total_couv_payant_selected'] / totals['total_couv_selected'],
            100.0 * totals['total_couv_off_selected'] / totals['total_couv_selected'],
            100.0,
        ],
        "Total Additions €": [
            totals['total_ca_selected'],
            totals['total_ca_offerts_selected'],
            totals['total_ca_selected'],
        ],
        "Panier moyen €": [
            panier_moyen['payants'],
            panier_moyen['offerts'],
            panier_moyen['total'],
        ],
    }

    result_df = pd.DataFrame(result_data).set_index('Types')

    format_dict = {
        'Nbr Couverts': '{:,.0f}'.replace(",", " "),
        '%': '{:.2f}',
        'Total Additions €': '{:,.2f}'.replace(",", " "),
        'Panier moyen €': '{:.2f}'
    }

    result_df1 = result_df.style.format(format_dict)

    return result_df, result_df1
