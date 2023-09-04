import pandas as pd
import holidays
from Clean_data import clean_file_in_folder
from Clean_data_snack import clean_file_in_folder_snack


def merged_data():
    brasserie_data = clean_file_in_folder()
    snack_data = clean_file_in_folder_snack()

    # Fusionner les DataFrames sur la colonne "Date" en utilisant 'outer'
    merged_df = brasserie_data.merge(snack_data, on="Date", how="outer")

    # Remplacer les valeurs NaN par 0
    merged_df = merged_df.fillna(0)

    # Regrouper par date et sommer les valeurs numériques
    merged_df = merged_df.groupby('Date').sum().reset_index()

    # # Convertir les colonnes contenant des chiffres au format numérique
    # numeric_columns = [
    #     "Diner_Covers_sales", "Diner_Price_sales", "Diner_Covers_intern", "Diner_Price_intern",
    #     "Dej_Covers_sales", "Dej_Price_sales", "Dej_Covers_intern", "Dej_Price_intern"
    # ]

    # merged_df[numeric_columns] = merged_df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # # Créer une fonction pour obtenir le jour de la semaine en français
    # def get_weekday_fr(date):
    #     jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    #     return jours[date.weekday()]

    # # Appliquer la fonction pour créer la colonne "Day"
    # merged_df["Day"] = merged_df["Date"].apply(get_weekday_fr)

    # # Initialiser le calendrier des jours fériés en France
    # fr_holidays = holidays.France()

    # # Ajouter la colonne "Ferie"
    # merged_df["Ferie"] = merged_df.apply(lambda row: 1 if row["Date"] in fr_holidays or (row["Date"] + pd.DateOffset(days=1)) in fr_holidays else 0, axis=1)

    # # Ajouter la colonne Diner_covers_total
    # merged_df['Diner_covers_total'] = merged_df['Diner_Covers_sales'] + merged_df['Diner_Covers_intern']

    # # Ajouter la colonne Dej_covers_total
    # merged_df['Dej_covers_total'] = merged_df['Dej_Covers_sales'] + merged_df['Dej_Covers_intern']

    # # Ajouter la colonne Covers_total
    # merged_df['Covers_total'] = merged_df['Diner_covers_total'] + merged_df['Dej_covers_total']

    # # Ajouter la colonne CA_total
    # merged_df['CA_total'] = merged_df['Diner_Price_sales'] + merged_df['Dej_Price_sales']


    return snack_data


if __name__ == '__main__':
    print(merged_data().Date.min())
