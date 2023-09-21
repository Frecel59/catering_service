# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Créez une fonction pour afficher un graphique avec filtre
def show_grouped_data(group_by, data_type, group_by_option, data_type_option, \
    month, filtered_df):
        days_order = ['Lundi',
                      'Mardi',
                      'Mercredi',
                      'Jeudi',
                      'Vendredi',
                      'Samedi',
                      'Dimanche']

        df_grouped = filtered_df.copy()
        if group_by == 'Jour':
            df_grouped['Jour'] = pd.Categorical(df_grouped['Jour'], \
                categories=days_order, ordered=True)
            grouped = df_grouped.groupby('Jour')[data_type].sum().reset_index()

        elif group_by == 'Mois et Jour' and month:
            df_grouped['mois'] = df_grouped['Date'].dt.to_period("M")
            df_grouped['Jour'] = pd.Categorical(df_grouped['Jour'], \
                categories=days_order, ordered=True)
            grouped = df_grouped[df_grouped['mois'].dt.strftime('%m/%Y') \
                == month].groupby(['mois', 'Jour'])[data_type].sum().reset_index()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(grouped['Jour'], grouped[data_type])
        ax.set_xlabel(group_by)
        ax.set_ylabel(data_type)
        ax.set_title(f"Répartition par {group_by_option} : {data_type_option}")

        # Utilisez set_xticks pour définir les positions des graduations
        ax.set_xticks(range(len(grouped['Jour'])))
        # Utilisez set_xticklabels pour définir les étiquettes des graduations
        ax.set_xticklabels(grouped['Jour'], rotation=45)

        st.pyplot(fig)
