import pandas as pd
import holidays
import os

# Chemin vers le dossier contenant les fichiers Excel
data_folder = 'Data'

def clean_file(excel_file_path): # Création d'une def qui va clean le fichier
    df = pd.read_excel(excel_file_path, engine='openpyxl')

    # Supprimer les lignes 0 à 9
    df.drop(range(10), inplace=True)

    # Liste des noms de colonnes à supprimer
    colonnes_a_supprimer = ['Rapport Brasserie Cedric', 'Unnamed: 6', 'Unnamed: 8', 'PASINO SAINT AMAND', 'Unnamed: 11', 'Unnamed: 13']

    # Supprimer les colonnes spécifiées
    df.drop(columns=colonnes_a_supprimer, inplace=True)

    # Création d'un dictionnaire de correspondance
    new_column_names = {
        'Unnamed: 0': 'Date',
        'Unnamed: 2': 'Diner_Covers_sales',
        'Unnamed: 3': 'Diner_Price_sales',
        'Unnamed: 4': 'Diner_Covers_intern',
        'Unnamed: 5': 'Diner_Price_intern',
        'Unnamed: 7': 'Dej_Covers_sales',
        'Unnamed: 9': 'Dej_Price_sales',
        'Unnamed: 12': 'Dej_Covers_intern',
        'Unnamed: 14': 'Dej_Price_intern'
    }

    # Renommer les colonnes en utilisant le dictionnaire de correspondance
    df.rename(columns=new_column_names, inplace=True)

    return df

def clean_file_in_folder(folder_path): # Création d'une def qui va concat tous les df cleaner
    all_dataframes = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.xlsx'):
            excel_file_path = os.path.join(folder_path, filename)
            df = clean_file(excel_file_path)
            all_dataframes.append(df)

    df = pd.concat(all_dataframes, ignore_index=True)

    # Convertir la colonne "Date" au format date
    df["Date"] = pd.to_datetime(df["Date"], format='%d/%m/%Y')

    # Convertir les colonnes contenant des chiffres au format numérique
    numeric_columns = [
        "Diner_Covers_sales", "Diner_Price_sales", "Diner_Covers_intern", "Diner_Price_intern",
        "Dej_Covers_sales", "Dej_Price_sales", "Dej_Covers_intern", "Dej_Price_intern"
    ]

    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Créer une fonction pour obtenir le jour de la semaine en français
    def get_weekday_fr(date):
        jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        return jours[date.weekday()]

    # Appliquer la fonction pour créer la colonne "Day"
    df["Day"] = df["Date"].apply(get_weekday_fr)

    # Initialiser le calendrier des jours fériés en France
    fr_holidays = holidays.France()

    # Ajouter la colonne "Ferie"
    df["Ferie"] = df.apply(lambda row: 1 if row["Date"] in fr_holidays or (row["Date"] + pd.DateOffset(days=1)) in fr_holidays else 0, axis=1)

    # Ajouter la colonne Diner_covers_total
    df['Diner_covers_total'] = df['Diner_Covers_sales'] + df['Diner_Covers_intern']

    # Ajouter la colonne Dej_covers_total
    df['Dej_covers_total'] = df['Dej_Covers_sales'] + df['Dej_Covers_intern']

    # Ajouter la colonne Covers_total
    df['Covers_total'] = df['Diner_covers_total'] + df['Dej_covers_total']

    # Ajouter la colonne CA_total
    df['CA_total'] = df['Diner_Price_sales'] + df['Dej_Price_sales']

    return df


# result_df = clean_file_in_folder(data_folder)

# # Enregistrer le DataFrame combiné dans un fichier Excel unique
# result_file_path = 'Data/concat/concat_data.xlsx'
# result_df.to_excel(result_file_path, index=False, engine='openpyxl')




if __name__ == '__main__':
    print(clean_file_in_folder(data_folder).Date.max())
