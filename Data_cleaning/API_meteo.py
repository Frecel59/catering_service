import pandas as pd
import requests
from datetime import datetime

from .Clean_data import clean_file_in_folder, data_folder



def historique_meteo(): # Création d'une def qui va récupérer les données météorologiques du dataset

    # Coordonnées GPS de l'établissement
    latitude = 50.45854187011719
    longitude = 3.428257942199707

    # Récupération de la date de début et fin du dataset
    start_date = clean_file_in_folder(data_folder).Date.min().date()
    end_date = clean_file_in_folder(data_folder).Date.max().date()

    # Données météo à récupérer
    variables = "temperature_2m,weathercode"

    url = f"https://archive-api.open-meteo.com/v1/era5?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&hourly={variables}"

    response = requests.get(url)
    data = response.json()

    hourly_data = data.get("hourly", {})
    time = hourly_data.get("time", [])
    temperature_2m = hourly_data.get("temperature_2m", [])
    weather_codes = hourly_data.get("weathercode", [])

    # Filtrer les données pour les heures 12 et 19 et stocker les résultats dans un DataFrame
    data_list = []
    for i in range(len(time)):
        if time[i].endswith("12:00") or time[i].endswith("19:00"):
            weather_code = weather_codes[i]

            # Analyser la date/heure au format ISO 8601
            dt_object = datetime.strptime(time[i], "%Y-%m-%dT%H:%M")
            date = dt_object.strftime("%Y-%m-%d")
            hour = dt_object.strftime("%H:%M")

            data_list.append({
                "Date": date,
                "Hour": hour,
                "Temperature": temperature_2m[i],
                "Weather Code": weather_code,
            })

    # Créer un DataFrame à partir de la liste de données
    df_meteo = pd.DataFrame(data_list)

    # Convertir la colonne "Date" au format date
    df_meteo["Date"] = pd.to_datetime(df_meteo["Date"])

    # Filtrer les données pour 12h et pour 19h et créer un DataFrame pour chaque
    df_meteo_12 = df_meteo[df_meteo["Hour"] == "12:00"].copy()
    df_meteo_19 = df_meteo[df_meteo["Hour"] == "19:00"].copy()

    return df_meteo_12, df_meteo_19

if __name__ == '__main__':
    print(historique_meteo())