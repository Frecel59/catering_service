# Importation des bibliothèques nécessaires
import pandas as pd
import os

# Importation des fichiers pour Snack
# Création d'une def qui va clean le fichier
def clean_file_snack(excel_file_path):
    df = pd.read_excel(excel_file_path, engine='openpyxl')

    # Supprimer les lignes 0 à 9
    df.drop(range(10), inplace=True)

    # Liste des noms de colonnes à supprimer
    colonnes_a_supprimer = ['Rapport Brasserie Cedric',
                            'Unnamed: 6',
                            'Unnamed: 8',
                            'PASINO SAINT AMAND',
                            'Unnamed: 11',
                            'Unnamed: 13']

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
    # Remplacer les NaN par 0
    df = df.fillna(0)

    # Convertir la colonne "Date" au format date
    df["Date"] = pd.to_datetime(df["Date"], format='%d/%m/%Y')

    return df

# Création d'une def qui va concat tous les df cleaner
def clean_file_in_folder_snack():
    all_dataframes = []
    data_folder = 'Data/snack'

    for filename in os.listdir(data_folder):
        if filename.endswith('.xlsx'):
            excel_file_path = os.path.join(data_folder, filename)
            df = clean_file_snack(excel_file_path)
            all_dataframes.append(df)

    df = pd.concat(all_dataframes, ignore_index=True)

    return df




if __name__ == '__main__':
    print(clean_file_in_folder_snack().Date.min())
