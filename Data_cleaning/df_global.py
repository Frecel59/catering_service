import pandas as pd

from .merged_data import merged_data
from .API_meteo import historique_meteo

# Créer une fonction de mapping pour les catégories météorologiques
def map_weather_category(code):
    if code == 0:
        return "Ciel Dégagé"
    elif code in [1, 2, 3]:
        return "Nuages"
    elif code in [45, 48, 51, 53, 55]:
        return "Précipitations Légères"
    elif code in [56, 57, 61, 63, 65]:
        return "Précipitations Modérées"
    elif code in [66, 67, 71, 73, 75, 77, 80, 81, 82]:
        return "Averses"
    elif code in [85, 86, 95, 96, 99]:
        return "Conditions Extrêmes"
    else:
        return "Inconnu"

def merge_dataframes():
    df_global = merged_data()
    df_meteo_12, df_meteo_19 = historique_meteo()

    df_global_merged = df_global.merge(df_meteo_12, on=["Date"], how="left")
    df_global_merged.rename(columns={
        "Temperature": "Temperature_12",
        "Weather Code": "Weather_Code_12"
        }, inplace=True)
    df_global_merged.drop('Hour', axis=1, inplace=True)

    df_global_merged = df_global_merged.merge(df_meteo_19, on=["Date"], how="left")
    df_global_merged.rename(columns={
        "Temperature": "Temperature_19",
        "Weather Code": "Weather_Code_19"
        }, inplace=True)
    df_global_merged.drop('Hour', axis=1, inplace=True)

    return df_global_merged

def rename_columns(df):
    new_column_names = {
        'Date': 'Date',
        'Day': 'Jour',
        'Diner_Covers_sales': 'Nbr couv. 19h',
        'Diner_Price_sales': 'Additions 19h',
        'Diner_Covers_intern': 'Nbr couv. off 19h',
        'Diner_Price_intern': 'Additions off 19h',
        'Dej_Covers_sales': 'Nbr couv 12h',
        'Dej_Price_sales': 'Additions 12h',
        'Dej_Covers_intern': 'Nbr couv. off 12h',
        'Dej_Price_intern': 'Additions off 12h',
        'Ferie': 'Féries',
        'Diner_covers_total': 'Nbr total couv. 19h',
        'Dej_covers_total': 'Nbr total couv. 12h',
        'Covers_total': 'Nbr total couv.',
        'CA_total': 'Total additions',
        'Server_total_12': 'Nbr serveurs 12h',
        'mean_server_12': 'Moy. serveurs 12h',
        'mean_server_19': 'Moy. serveurs 19h',
        'Server_total_19': 'Nbr serveurs 19h',
        'Server_total': 'Nbr total serveurs',
        'Temperature_12': 'Temp. 12h',
        'Temperature_19': 'Temp. 19h',
        'Weather_19': 'Méteo 19h',
        'Weather_12': 'Météo 12h'
    }

    df.rename(columns=new_column_names, inplace=True)
    return df

def merged_df():
    df_global_merged = merge_dataframes()

    df_global_merged["Weather_12"] = df_global_merged["Weather_Code_12"].apply(map_weather_category)
    df_global_merged["Weather_19"] = df_global_merged["Weather_Code_19"].apply(map_weather_category)

    colonnes_a_supprimer = ['Weather_Code_12', 'Weather_Code_19']
    df_global_merged.drop(columns=colonnes_a_supprimer, inplace=True)

    df_final = rename_columns(df_global_merged)

    return df_final

if __name__ == '__main__':
    print(merged_df())
