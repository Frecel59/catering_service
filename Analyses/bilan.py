import pandas as pd

def analyses_bilan(jours_moments_selectionnes, filtered_vsd):
    def calculate_totals(filtered_vsd, column_prefix):
        totals = pd.Series(0, index=filtered_vsd.index)
        for moment in ['12h', '19h']:
            mask = filtered_vsd['Jour'].map(jours_moments_selectionnes).apply(lambda x: moment in x)
            totals += filtered_vsd.loc[mask, f'{column_prefix} {moment}']
        return totals

    total_columns = [f'Total_{col}' for col in ['Couv', 'Couv_Off', 'CA', 'CA_Offerts']]
    column_prefixes = ['Nbr couv.', 'Nbr couv. off', 'Additions', 'Additions off']

    for total_col, col_prefix in zip(total_columns, column_prefixes):
        filtered_vsd[total_col] = calculate_totals(filtered_vsd, col_prefix)

    total_couv_selected = filtered_vsd['Total_Couv'].sum()
    total_couv_off_selected = filtered_vsd['Total_Couv_Off'].sum()
    total_couv_payant_selected = total_couv_selected - total_couv_off_selected

    percent_total_couv_off_selected = 100 * total_couv_off_selected / total_couv_selected if total_couv_selected != 0 else 0
    percent_total_couv_payant_selected = 100 * total_couv_payant_selected / total_couv_selected if total_couv_selected != 0 else 0

    total_ca_selected = filtered_vsd['Total_CA'].sum()
    total_ca_offerts_selected = filtered_vsd['Total_CA_Offerts'].sum()

    panier_moyen_selected = total_ca_selected / total_couv_selected if total_couv_selected != 0 else None
    panier_moyen_payants_selected = total_ca_selected / total_couv_payant_selected if total_couv_payant_selected != 0 else None
    panier_moyen_off_selected = total_ca_offerts_selected / total_couv_off_selected if total_couv_off_selected != 0 else None


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
    result_df1['Panier moyen €'] = result_df1['Panier moyen €'].apply(lambda x: f"{x:.2f}" if x is not None else '-')

    return result_df, result_df1
