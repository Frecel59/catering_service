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

    categories_a_supprimer = ['ACC GRATUIT', 'DIVERS', 'DIVERS SOFT', 'BANQUET']

    # Créer un masque pour les lignes à supprimer
    masque_suppression = merged_df_ventes['Catégorie'].isin(categories_a_supprimer)

    # Appliquer le masque pour supprimer les lignes
    merged_df_ventes = merged_df_ventes[~masque_suppression]

    # Créer un dictionnaire de correspondance entre Catégorie et Famille
    correspondance_famille = {
        'PLATS': 'PLATS',
        'DESSERTS': 'DESSERTS',
        'VINS': 'VINS',
        'ENTREES': 'ENTREES',
        'BIERES': 'BIERES',
        'AUTRES': 'PLATS',
        'COCKTAILS ALCOOLS': 'ALCOOLS',
        'APERITIFS': 'ALCOOLS',
        'CHAMPAGNES': 'VINS',
        'EAUX': 'SOFT',
        'SODA BTL': 'SOFT',
        'ALCOOLS': 'ALCOOLS',
        'CAFETERIE': 'CAFETERIE',
        'SODA VERRE': 'SOFT',
        'COCKTAILS SS/ALCOOLS': 'SOFT',
        'DIGESTIFS': 'ALCOOLS',
        'JUS DE FRUITS': 'SOFT',
        'FROMAGES': 'DESSERTS',
        'SIROPS': 'SOFT',
        'MENU FORMULE': 'MENUS'
    }

    # Ajouter une nouvelle colonne "Famille" basée sur la correspondance
    merged_df_ventes['Famille'] = merged_df_ventes['Catégorie'].map(correspondance_famille)



    return merged_df_ventes


if __name__ == '__main__':
    print(merged_data_ventes().Date.max())
