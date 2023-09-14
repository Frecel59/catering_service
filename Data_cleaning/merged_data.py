# Importation des bibliothèques nécessaires
import pandas as pd
import holidays

# Importation des fonctions personnalisées depuis d'autres fichiers Python
from datetime import timedelta
from .Clean_data import clean_file_in_folder
from .Clean_data_snack import clean_file_in_folder_snack


def merged_data():
    brasserie_data = clean_file_in_folder()
    snack_data = clean_file_in_folder_snack()

    # Fusionner les deux DataFrames en utilisant concat
    merged_df = pd.concat([brasserie_data, snack_data], ignore_index=True)

    # Regrouper par date et sommer les colonnes numériques
    merged_df = merged_df.groupby('Date').sum().reset_index()


    # Créer une fonction pour obtenir le jour de la semaine en français
    def get_weekday_fr(date):
        jours = ["Lundi",
                 "Mardi",
                 "Mercredi",
                 "Jeudi",
                 "Vendredi",
                 "Samedi",
                 "Dimanche"]
        return jours[date.weekday()]

    # Appliquer la fonction pour créer la colonne "Day"
    merged_df["Day"] = merged_df["Date"].apply(get_weekday_fr)

    # Initialiser le calendrier des jours fériés en France
    fr_holidays = holidays.France()

    # Ajouter la colonne "Ferie"
    merged_df["Ferie"] = merged_df.apply(lambda row: 1 if row["Date"] in \
        fr_holidays or (row["Date"] + pd.DateOffset(days=1)) in fr_holidays \
            else 0, axis=1)

    # Ajouter la colonne Diner_covers_total
    merged_df['Diner_covers_total'] = merged_df['Diner_Covers_sales'] + \
        merged_df['Diner_Covers_intern']

    # Ajouter la colonne Dej_covers_total
    merged_df['Dej_covers_total'] = merged_df['Dej_Covers_sales'] + \
        merged_df['Dej_Covers_intern']

    # Ajouter la colonne Covers_total
    merged_df['Covers_total'] = merged_df['Diner_covers_total'] + \
        merged_df['Dej_covers_total']

    # Ajouter la colonne CA_total
    merged_df['CA_total'] = merged_df['Diner_Price_sales'] + \
        merged_df['Dej_Price_sales']

    # Ajouter la colonne Server_total_12
    merged_df['Server_total_12'] = merged_df['Dej_covers_total'] / 25

    # Ajouter la colonne Server_total_19
    merged_df['Server_total_19'] = merged_df['Diner_covers_total'] / 25

    # Ajouter la colonne Server_total
    merged_df['Server_total'] = merged_df['Covers_total'] / 25


    # Créez une colonne pour stocker les moyennes
    merged_df['mean_server_12'] = 0.0

    # Parcourez les lignes du DataFrame
    for index, row in merged_df.iterrows():
        current_date = row['Date']
        previous_date = current_date - timedelta(days=7)
        next_date = current_date + timedelta(days=7)

        # Filtrage des données pour les dates correspondantes
        relevant_data = merged_df[(merged_df['Date'] == current_date) |
                                (merged_df['Date'] == previous_date) |
                                (merged_df['Date'] == next_date)]

        # Calcul de la moyenne et assignation à la ligne actuelle
        mean = relevant_data['Server_total_12'].mean()
        merged_df.at[index, 'mean_server_12'] = round(mean, 2)

    # Créez une colonne pour stocker les moyennes
    merged_df['mean_server_19'] = 0.0

    # Parcourez les lignes du DataFrame
    for index, row in merged_df.iterrows():
        current_date = row['Date']
        previous_date = current_date - timedelta(days=7)
        next_date = current_date + timedelta(days=7)

        # Filtrage des données pour les dates correspondantes
        relevant_data = merged_df[(merged_df['Date'] == current_date) |
                                (merged_df['Date'] == previous_date) |
                                (merged_df['Date'] == next_date)]

        # Calcul de la moyenne et assignation à la ligne actuelle
        mean = relevant_data['Server_total_19'].mean()
        merged_df.at[index, 'mean_server_19'] = round(mean, 2)


    return merged_df


if __name__ == '__main__':
    print(merged_data().Date.max())
