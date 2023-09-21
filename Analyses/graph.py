# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Créez une fonction pour afficher un graphique avec filtre
def show_grouped_data(group_by, data_type, group_by_option, data_type_option, month, filtered_df):
    days_order = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

    df_grouped = filtered_df.copy()
    if group_by == 'Jour':
        df_grouped['Jour'] = pd.Categorical(df_grouped['Jour'], categories=days_order, ordered=True)
        grouped = df_grouped.groupby('Jour')[data_type].sum().reset_index()

    elif group_by == 'Mois et Jour' and month:
        df_grouped['mois'] = df_grouped['Date'].dt.to_period("M")
        df_grouped['Jour'] = pd.Categorical(df_grouped['Jour'], categories=days_order, ordered=True)
        grouped = df_grouped[df_grouped['mois'].dt.strftime('%m/%Y') == month].groupby(['mois', 'Jour'])[data_type].sum().reset_index()

    # Création d'un graphique bar avec Plotly
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grouped['Jour'],
        y=grouped[data_type],
        name=data_type_option
    ))
    fig.update_layout(
        title=f"Répartition par {group_by_option} : {data_type_option}",
        xaxis_title=group_by,
        yaxis_title=data_type,
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig)
