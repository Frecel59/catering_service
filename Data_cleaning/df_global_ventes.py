# Importation des bibliothèques nécessaires
import pandas as pd

# Importation des fonctions personnalisées depuis d'autres fichiers Python
from .Clean_ventes import clean_files_in_bucket_ventes
from .Clean_ventes_snack import clean_files_in_bucket_ventes_snack


def merged_data_ventes():
    brasserie_data_ventes = clean_files_in_bucket_ventes()
    snack_data_ventes = clean_files_in_bucket_ventes_snack()

    # Fusionner les deux DataFrames en utilisant concat
    merged_df_ventes = pd.concat([brasserie_data_ventes, snack_data_ventes], ignore_index=True)

    # Grouper par 'Date', 'Catégorie', et 'Produit' et faire la somme des colonnes numériques
    merged_df_ventes = merged_df_ventes.groupby(['Date', 'Catégorie', 'Produit']).sum().reset_index()



    return merged_df_ventes


if __name__ == '__main__':
    print(merged_data_ventes().Date.max())
