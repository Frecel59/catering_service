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


    # Grouper par 'Famille' et sommer les 'Prix' et 'Quantité'
    prix_total_par_famille = df.groupby('Famille').agg({'Prix': 'sum', 'Quantité': 'sum'})

    # Calculer le total global des 'Prix'
    total_global = prix_total_par_famille['Prix'].sum()

    # Ajouter une nouvelle colonne pour le pourcentage du total
    prix_total_par_famille['% du Total'] = (prix_total_par_famille['Prix'] / total_global) * 100

    # Calculer la moyenne là où Quantité n'est pas égale à zéro, mettre zéro ailleurs
    mask = prix_total_par_famille['Quantité'] != 0
    prix_total_par_famille.loc[mask, 'Prix Moyen'] = prix_total_par_famille.loc[mask, 'Prix'] / prix_total_par_famille.loc[mask, 'Quantité']
    prix_total_par_famille.loc[~mask, 'Prix Moyen'] = np.nan  # ou np.nan si vous préférez

    # Trier le DataFrame par 'Prix' en ordre décroissant si nécessaire
    prix_total_par_famille = prix_total_par_famille.sort_values(by='Prix', ascending=False)

    # Appliquez 'format_percent' à chaque cellule de la colonne "% du Total" '.
    prix_total_par_famille["% du Total"] = prix_total_par_famille["% du Total"].map(format_percent)

    # Pour chaque colonne, appliquez 'format_numbers' à chaque cellule de la colonne.
    for col in ['Prix', 'Prix Moyen']:
        prix_total_par_famille[col] = prix_total_par_famille[col].map(format_numbers)


    return prix_total_par_famille

def display_dataframe_famille(filtered_df):
    df = filtered_df

    # Dropdown widget
    famille = sorted(df['Famille'].dropna().unique().tolist())

    selected_famille = st.selectbox("Famille:", famille)

    # Filtrer et trier le DataFrame en fonction de la catégorie sélectionnée
    df_choice_famille = df[df['Famille'] == selected_famille]
    df_choice_famille = df_choice_famille.groupby('Produit').agg({'Quantité': 'sum', 'Prix': 'sum'})
    df_choice_famille = df_choice_famille.sort_values(by='Quantité', ascending=False)

    # Pour chaque colonne, appliquez 'format_numbers' à chaque cellule de la colonne.
    for col in ['Prix']:
        df_choice_famille[col] = df_choice_famille[col].map(format_numbers)

    return df_choice_famille

def display_dataframe_categorie(filtered_df):
    df = filtered_df

    # Dropdown widget
    categories = sorted(df['Catégorie'].unique().tolist())
    selected_category = st.selectbox("Catégorie:", categories)

    # Filtrer et trier le DataFrame en fonction de la catégorie sélectionnée
    df_choice = df[df['Catégorie'] == selected_category]
    df_choice = df_choice.groupby('Produit').agg({'Quantité': 'sum', 'Prix': 'sum'})
    df_choice = df_choice.sort_values(by='Quantité', ascending=False)

    # Pour chaque colonne, appliquez 'format_numbers' à chaque cellule de la colonne.
    for col in ['Prix']:
        df_choice[col] = df_choice[col].map(format_numbers)

    return df_choice
