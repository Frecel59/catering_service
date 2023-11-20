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
    dropdown = widgets.Dropdown(options=categories, value=categories[0], description='Catégorie:')
    output = widgets.Output()

    def on_change(change):
        if change['type'] == 'change' and change['name'] == 'value':
            # Lorsque la valeur du dropdown change, filtre et trie le DataFrame
            with output:
                clear_output(wait=True)
                selected_category = change['new']
                df_choice = df[df['Catégorie'] == selected_category]
                df_choice = df_choice.head(50).sort_values(by='Quantité', ascending=False)  # Tri le DataFrame filtré
                display(df_choice)  # Utilise display au lieu de print

    dropdown.observe(on_change)
    display(dropdown, output)
