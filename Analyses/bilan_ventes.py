# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd
import numpy as np
import ipywidgets as widgets
from IPython.display import display, clear_output

def format_percent(value):
        if isinstance(value, (int, float)):
            return f"{value:,.2f}%".replace(",", " ").replace(".", ",")
        else:
            return value

def format_numbers(value):
    if isinstance(value, (int, float)):
        if value.is_integer():
            return f"{value:,.0f}".replace(",", " ")
        else:
            return f"{value:,.2f}".replace(",", " ").replace(".", ",")
    else:
        return value


def analyses_bilan_ventes (filtered_df):
    df = filtered_df

    categories_a_supprimer = ['ACC GRATUIT', 'DIVERS', 'DIVERS SOFT', 'BANQUET']

    # Créer un masque pour les lignes à supprimer
    masque_suppression = df['Catégorie'].isin(categories_a_supprimer)

    # Appliquer le masque pour supprimer les lignes
    df = df[~masque_suppression]

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
    df['Famille'] = df['Catégorie'].map(correspondance_famille)

    # Grouper par 'Catégorie' et sommer les 'Prix' et 'Quantité'
    prix_total_par_categorie = df.groupby('Famille').agg({'Prix': 'sum', 'Quantité': 'sum'})

    # Calculer le total global des 'Prix'
    total_global = prix_total_par_categorie['Prix'].sum()

    # Ajouter une nouvelle colonne pour le pourcentage du total
    prix_total_par_categorie['% du Total'] = (prix_total_par_categorie['Prix'] / total_global) * 100

    # Calculer la moyenne là où Quantité n'est pas égale à zéro, mettre zéro ailleurs
    mask = prix_total_par_categorie['Quantité'] != 0
    prix_total_par_categorie.loc[mask, 'Prix Moyen'] = prix_total_par_categorie.loc[mask, 'Prix'] / prix_total_par_categorie.loc[mask, 'Quantité']
    prix_total_par_categorie.loc[~mask, 'Prix Moyen'] = np.nan  # ou np.nan si vous préférez

    # Trier le DataFrame par 'Prix' en ordre décroissant si nécessaire
    prix_total_par_categorie = prix_total_par_categorie.sort_values(by='Prix', ascending=False)

    # Appliquez 'format_percent' à chaque cellule de la colonne "% du Total" '.
    prix_total_par_categorie["% du Total"] = prix_total_par_categorie["% du Total"].map(format_percent)

    # Pour chaque colonne, appliquez 'format_numbers' à chaque cellule de la colonne.
    for col in ['Prix', 'Prix Moyen']:
        prix_total_par_categorie[col] = prix_total_par_categorie[col].map(format_numbers)


    return prix_total_par_categorie

def display_dataframe_with_dropdown(filtered_df):
    df = filtered_df

    # Dropdown widget
    categories = sorted(df['Catégorie'].unique().tolist())
    selected_category = st.selectbox("Catégorie:", categories)

    # Filtrer et trier le DataFrame en fonction de la catégorie sélectionnée
    df_choice = df[df['Catégorie'] == selected_category]
    df_choice = df_choice.groupby('Produit').agg({'Quantité': 'sum', 'Prix': 'sum'})
    df_choice = df_choice.sort_values(by='Quantité', ascending=False).head(50)

    # Pour chaque colonne, appliquez 'format_numbers' à chaque cellule de la colonne.
    for col in ['Prix']:
        df_choice[col] = df_choice[col].map(format_numbers)

    return df_choice
