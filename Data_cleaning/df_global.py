import pandas as pd

from .Clean_data import clean_file_in_folder, data_folder
from .API_meteo import historique_meteo


def merged_df(): # Création d'une def qui va merged le dataframe avec ceux de la météo 12h et 19h

    df_global = clean_file_in_folder(data_folder)
    df_meteo_12, df_meteo_19 = historique_meteo()

    # Fusionner les DataFrames en fonction de la colonne "Date"
    df_global_merged = df_global.merge(df_meteo_12, on=["Date"], how="left")
    df_global_merged.rename(columns={"Temperature": "Temperature_12", "Weather Code": "Weather_Code_12"}, inplace=True)
    df_global_merged.drop('Hour', axis=1, inplace=True)

    df_global_merged = df_global_merged.merge(df_meteo_19, on=["Date"], how="left")
    df_global_merged.rename(columns={"Temperature": "Temperature_19", "Weather Code": "Weather_Code_19"}, inplace=True)
    df_global_merged.drop('Hour', axis=1, inplace=True)

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

    # Appliquer la fonction de mapping pour créer la colonne Weather_12 et Weather_19
    df_global_merged["Weather_12"] = df_global_merged["Weather_Code_12"].apply(map_weather_category)
    df_global_merged["Weather_19"] = df_global_merged["Weather_Code_19"].apply(map_weather_category)

    return df_global_merged


if __name__ == '__main__':
    print(merged_df())
