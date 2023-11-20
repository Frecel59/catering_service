import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import io
import matplotlib.pyplot as plt

from gcp import get_storage_client
from utils import display_icon
from Analyses.graph import show_grouped_data
import footer


def format_date_in_french(date):
    mois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet',
            'août', 'septembre', 'octobre', 'novembre', 'décembre']
    return f"{date.day} {mois[date.month - 1]} {date.year}"


def get_df_from_gcp():
    client, bucket = get_storage_client()
    blob_path = "DF_FINALE/COVERS_df_finale.xlsx"
    blob = bucket.blob(blob_path)
    in_memory_file = io.BytesIO()
    blob.download_to_file(in_memory_file)
    in_memory_file.seek(0)
    df = pd.read_excel(in_memory_file)
    return df


def plot_graph(df, column, options, title, color_map=None):
    selected_options = st.multiselect(f"Sélectionnez les courbes à afficher :", options, default=options)
    if selected_options:
        fig = px.line(df, x="Date", y=selected_options, title=title, color_discrete_map=color_map)
        fig.update_xaxes(tickformat="%m-%Y")
        st.plotly_chart(fig)
    else:
        st.write(f"Veuillez sélectionner au moins une option pour afficher le graphique.")


def get_df_filtered():
    with open('style.css', 'r') as css_file:
        css = css_file.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    df_final = get_df_from_gcp()
    st.markdown(f'<p class="period-text">Choississez une période</p>', unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col3:
        start_date = st.date_input("Date de départ", datetime((df_final["Date"].max()).year - 1, 11, 1),
                                   key="start_date_input", format="DD/MM/YYYY")
    with col4:
        end_date = st.date_input("Date de fin", df_final["Date"].max(),
                                 key="end_date_input", format="DD/MM/YYYY")

    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)
    filtered_df = df_final[(df_final["Date"] >= pd.to_datetime(start_date)) &
                           (df_final["Date"] <= pd.to_datetime(end_date))]
    return filtered_df


def main():
    display_icon("Dashboard", "Dashboard")
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)
    df = get_df_filtered()


    # 1. Analyse des couverts
    st.title("1. Analyse des couverts")

    df_report = df

    days_order = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    df_report['Jour'] = pd.Categorical(df_report['Jour'], categories=days_order, ordered=True)


    color_map_bar = {
        "Nbr couv. 12h": "#FFA726",
        "Nbr couv. 19h": "#5C6BC0",
        "Nbr couv. off 12h": "#AB47BC",
        "Nbr couv. off 19h": "#26A69A",
        "Nbr total couv. 19h": "#5C6BC0",
        "Nbr total couv. 12h": "#FFA726",
        "Additions 12h": "#FFA726",
        "Additions 19h": "#5C6BC0",
        "Total additions": "#5C6BC0",
        "Panier moyen 12h": "#FFA726",
        "Panier moyen 19h": "#5C6BC0",
        "Nbr serveurs 12h": "#FFA726",
        "Nbr serveurs 19h": "#5C6BC0",
    }
    # Création des colonnes
    col1, col2 = st.columns(2)

    # Graphique dans la colonne 1: Total des couverts payants
    with col1:
        st.markdown("### Nbr total de couverts (facturés)")
        fig = px.bar(
            df_report.groupby('Jour')[['Nbr couv. 12h', 'Nbr couv. 19h']].sum().reset_index(),
            x='Jour',
            y=['Nbr couv. 12h', 'Nbr couv. 19h'],
            color_discrete_map=color_map_bar
        )
        st.plotly_chart(fig)


    # Graphique dans la colonne 2: Total des couverts offerts
    with col2:
        st.markdown("### Nbr total de couverts (offerts)")
        fig = px.bar(
            df_report.groupby('Jour')[['Nbr couv. off 12h', 'Nbr couv. off 19h']].sum().reset_index(),
            x='Jour',
            y=['Nbr couv. off 12h', 'Nbr couv. off 19h'],
            color_discrete_map=color_map_bar
        )
        st.plotly_chart(fig)

    # Création de nouvelles colonnes
    col1, col2 = st.columns(2)

    # Graphique dans la colonne 1: Répartition des couverts offerts vs payants à 12h
    with col1:
        st.markdown("### Répartition des couverts offerts vs payants à 12h")
        fig = px.bar(
            df_report.groupby('Jour')[['Nbr couv. 12h', 'Nbr couv. off 12h']].sum().reset_index(),
            x='Jour',
            y=['Nbr couv. 12h', 'Nbr couv. off 12h'],
            color_discrete_map=color_map_bar
        )
        st.plotly_chart(fig)

    # Graphique dans la colonne 2: Répartition des couverts offerts vs payants à 19h
    with col2:
        st.markdown("### Répartition des couverts offerts vs payants à 19h")
        fig = px.bar(
            df_report.groupby('Jour')[['Nbr couv. 19h', 'Nbr couv. off 19h']].sum().reset_index(),
            x='Jour',
            y=['Nbr couv. 19h', 'Nbr couv. off 19h'],
            color_discrete_map=color_map_bar
        )
        st.plotly_chart(fig)

    # Graphique dans la colonne 1: Tendance des couverts à 12h
    with col1:
        st.markdown("### Tendance des couverts à 12h")
        fig = px.line(
            df_report,
            x='Date',
            y='Nbr total couv. 12h',
            color_discrete_sequence=[color_map_bar["Nbr total couv. 12h"]]
        )
        fig.update_xaxes(tickformat="%d-%m-%y")
        st.plotly_chart(fig)

    # Graphique dans la colonne 2: Tendance des couverts à 19h
    with col2:
        st.markdown("### Tendance des couverts à 19h")
        fig = px.line(
            df_report,
            x='Date',
            y='Nbr total couv. 19h',
            color_discrete_sequence=[color_map_bar["Nbr total couv. 19h"]]
        )
        fig.update_xaxes(tickformat="%d-%m-%y")
        st.plotly_chart(fig)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # 2. Analyse des additions
    st.title("2. Analyse des additions")

    # Création des colonnes
    col1, col2 = st.columns(2)

    # Graphique dans la colonne 1: Total des additions
    with col1:
        st.markdown("### Total des additions")
        fig = px.bar(
            df_report.groupby('Jour')[['Additions 12h','Additions 19h']].sum().reset_index(),
            x='Jour',
            y=['Additions 12h','Additions 19h'],
            color_discrete_map=color_map_bar
        )
        st.plotly_chart(fig)

    # Création des colonnes
    col1, col2 = st.columns(2)
    # Graphique dans la colonne 1: Tendance des additions à 12h
    with col1:
        st.markdown("### Tendance des additions à 12h")
        fig = px.line(
            df_report,
            x='Date',
            y='Additions 12h',
            color_discrete_sequence=[color_map_bar["Additions 12h"]]
        )
        fig.update_xaxes(tickformat="%d-%m-%y")
        st.plotly_chart(fig)
    # Graphique dans la colonne 2: Tendance des additions à 19h
    with col2:
        st.markdown("### Tendance des additions à 19h")
        fig = px.line(
            df_report,
            x='Date',
            y='Additions 19h',
            color_discrete_sequence=[color_map_bar["Additions 19h"]]
        )
        fig.update_xaxes(tickformat="%d-%m-%y")
        st.plotly_chart(fig)


    st.markdown("<hr/>", unsafe_allow_html=True)

    # 3. Analyse du panier moyen
    st.title("3. Analyse du panier moyen")

    # Création des colonnes
    col1, col2 = st.columns(2)
    # Graphique dans la colonne 1: Tendance du panier moyen à 12h
    with col1:
        st.markdown("### Tendance du panier moyen à 12h")
        fig = px.line(
            df_report,
            x='Date',
            y='Panier moyen 12h',
            color_discrete_sequence=[color_map_bar["Panier moyen 12h"]]
        )
        fig.update_xaxes(tickformat="%d-%m-%y")
        st.plotly_chart(fig)

    # Graphique dans la colonne 2: Tendance du panier moyen à 19h
    with col2:
        st.markdown("### Tendance du panier moyen à 19h")
        fig = px.line(
            df_report,
            x='Date',
            y='Panier moyen 19h',
            color_discrete_sequence=[color_map_bar["Panier moyen 19h"]]
        )
        fig.update_xaxes(tickformat="%d-%m-%y")
        st.plotly_chart(fig)


    st.markdown("<hr/>", unsafe_allow_html=True)

    # 4. Analyse du nbr de serveurs
    st.title("4. Analyse du nbr de serveurs")

    # Création des colonnes
    col1, col2 = st.columns(2)
    # Graphique dans la colonne 1: Total des additions
    with col1:
        st.markdown("### Total nbr serveurs")
        fig = px.bar(
            df_report.groupby('Jour')[['Nbr serveurs 12h','Nbr serveurs 19h']].sum().reset_index(),
            x='Jour',
            y=['Nbr serveurs 12h','Nbr serveurs 19h'],
            color_discrete_map=color_map_bar
        )
        st.plotly_chart(fig)

    # Création des colonnes
    col1, col2 = st.columns(2)
    # Graphique dans la colonne 1: Tendance du nbr de serveur à 12h
    with col1:
        st.markdown("### Tendance du nbr de serveur à 12h")
        fig = px.line(
            df_report,
            x='Date',
            y='Nbr serveurs 12h',
            color_discrete_sequence=[color_map_bar["Nbr serveurs 12h"]]
        )
        fig.update_xaxes(tickformat="%d-%m-%y")
        st.plotly_chart(fig)

    # Graphique dans la colonne 2: Tendance du nbr de serveur à 19h
    with col2:
        st.markdown("### Tendance du nbr de serveur à 19h")
        fig = px.line(
            df_report,
            x='Date',
            y='Nbr serveurs 19h',
            color_discrete_sequence=[color_map_bar["Nbr serveurs 19h"]]
        )
        fig.update_xaxes(tickformat="%d-%m-%y")
        st.plotly_chart(fig)


    st.markdown("<hr/>", unsafe_allow_html=True)

    # 5. Analyse de la météo
    st.title("5. Analyse de la météo")

    # Création des colonnes
    col1, col2 = st.columns(2)

    # Filtrage des données pour exclure les rangées où 'Météo 12h' est 'Inconnu'
    filtered_df_report_12 = df_report[df_report['Météo 12h'] != 'Inconnu']

    # Graphique dans la colonne 1: Influence de la météo sur le nombre de couverts à 12h
    with col1:
        st.markdown("### Influence de la météo sur le nbr de couverts à 12h")
        fig = px.bar(
            filtered_df_report_12.groupby('Météo 12h', observed=True)['Nbr total couv. 12h'].sum().reset_index(),
            x='Météo 12h',
            y='Nbr total couv. 12h',
            color_discrete_sequence=[color_map_bar["Nbr total couv. 12h"]]
        )
        st.plotly_chart(fig)

    df_report['Méteo 19h'] = df_report['Méteo 19h'].astype(str)
    filtered_df_report_19 = df_report[df_report['Méteo 19h'] != 'Inconnu']

    # Graphique dans la colonne 2: Influence de la météo sur le nombre de couverts à 19h
    with col2:
        st.markdown("### Influence de la météo sur le nbr de couverts à 19h")
        fig = px.bar(
            filtered_df_report_19.groupby('Méteo 19h')['Nbr total couv. 19h'].sum().reset_index(),
            x='Méteo 19h',
            y='Nbr total couv. 19h',
            color_discrete_sequence=[color_map_bar["Nbr total couv. 19h"]]
        )
        st.plotly_chart(fig)

    # Graphique dans la colonne 1: Influence de la température sur le nombre de couverts à 12h
    with col1:
        st.markdown("### Influence de la température sur le nbr de couverts à 12h")
        fig = px.bar(
            df_report.groupby('Temp. 12h')['Nbr total couv. 12h'].sum().reset_index(),
            x='Temp. 12h',
            y='Nbr total couv. 12h',
            color_discrete_sequence=[color_map_bar["Nbr total couv. 12h"]]
        )
        st.plotly_chart(fig)

    # Graphique dans la colonne 2: Influence de la température sur le nombre de couverts à 19h
    with col2:
        st.markdown("### Influence de la température sur le nbr de couverts à 19h")
        fig = px.bar(
            df_report.groupby('Temp. 19h')['Nbr total couv. 19h'].sum().reset_index(),
            x='Temp. 19h',
            y='Nbr total couv. 19h',
            color_discrete_sequence=[color_map_bar["Nbr total couv. 19h"]]
        )
        st.plotly_chart(fig)

    st.markdown("<hr/>", unsafe_allow_html=True)




    footer.display()

if __name__ == "__main__":
    main()
