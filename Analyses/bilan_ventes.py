# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd
import numpy as np
import ipywidgets as widgets
from IPython.display import display, clear_output


def analyses_bilan_ventes (filtered_df):
    df = filtered_df

    # Grouper par 'Catégorie' et sommer les 'Prix' et 'Quantité'
    prix_total_par_categorie = df.groupby('Catégorie').agg({'Prix': 'sum', 'Quantité': 'sum'}).reset_index()

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



    return prix_total_par_categorie

def display_dataframe_with_dropdown(df):
    # Dropdown widget
    categories = sorted(df['Catégorie'].unique().tolist())
    selected_category = st.selectbox("Catégorie:", categories)

    # Filtrer et trier le DataFrame en fonction de la catégorie sélectionnée
    df_choice = df[df['Catégorie'] == selected_category]
    df_choice = df_choice.head(50).sort_values(by='Quantité', ascending=False)

    # Afficher le DataFrame
    st.table(df_choice)
