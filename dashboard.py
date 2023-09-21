import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import io
from gcp import get_storage_client
from utils import display_icon
from Analyses.graph import show_grouped_data


def format_date_in_french(date):
    mois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet',
            'août', 'septembre', 'octobre', 'novembre', 'décembre']
    return f"{date.day} {mois[date.month - 1]} {date.year}"


def get_df_from_gcp():
    client, bucket = get_storage_client()
    blob_path = "COVERS_BRASSERIE_DF_FINALE/df_finale.xlsx"
    blob = bucket.blob(blob_path)
    in_memory_file = io.BytesIO()
    blob.download_to_file(in_memory_file)
    in_memory_file.seek(0)
    df = pd.read_excel(in_memory_file)
    return df


def plot_graph(df, column, options, title):
    selected_options = st.multiselect(f"Sélectionnez les courbes à afficher :", options, default=options)
    if selected_options:
        fig = px.line(df, x="Date", y=selected_options, title=title)
        st.plotly_chart(fig)
    else:
        st.write(f"Veuillez sélectionner au moins une option pour afficher le graphique.")

def plot_grouped_bar(df, x_column, y_columns, title, labels):
    fig = px.bar(df, x=x_column, y=y_columns, title=title, labels=labels)
    st.plotly_chart(fig)

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
    display_icon("Dashboard", "Tableau d'analyses")
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)
    df = get_df_filtered()

    st.subheader("Analyse Temporelle")
    col1_graph1, col2_graph2 = st.columns(2)
    with col1_graph1:
        plot_graph(df, "Graphique 1", ["Nbr total couv. 19h", "Nbr total couv. 12h"], 'Évolution du nbr de couverts payants')
    with col2_graph2:
        plot_graph(df, "Graphique 2", ["Nbr couv. off 12h", "Nbr couv. off 19h"], 'Évolution du nbr de couverts offerts')

    col1_graph3, col2_graph4 = st.columns(2)
    with col1_graph3:
        plot_graph(df, "Graphique 3", ["Panier moyen 12h", "Panier moyen 19h", "Panier moyen jour"], 'Évolution du panier moyen')
    with col2_graph4:
        plot_graph(df, "Graphique 4", ["Additions 19h", "Additions 12h", "Total additions"], 'Évolution du CA')

    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    st.subheader("Répartition")
    col1_graph5, col2_graph6 = st.columns(2)
    with col1_graph5:
        # Sélecteur pour permettre à l'utilisateur de choisir l'option
        selected_couverts = st.selectbox("Sélectionnez le filtre :", ["Nbr total couv. 12h", "Nbr total couv. 19h", "Nbr total couv."])
        fig = px.histogram(df, x=selected_couverts, title=f"Distribution : {selected_couverts}")
        st.plotly_chart(fig)
    with col2_graph6:
        # Sélecteur pour permettre à l'utilisateur de choisir l'option
        selected_addition = st.selectbox("Sélectionnez le filtre :", ["Additions 12h", "Additions 19h", "Total additions"])
        fig = px.histogram(df, x=selected_addition, title=f"Distribution : {selected_addition}")
        st.plotly_chart(fig)

    col1_graph7, col2_graph8 = st.columns(2)
    with col1_graph7:
        # Sélecteur pour permettre à l'utilisateur de choisir l'option
        selected_panier = st.selectbox("Sélectionnez le filtre :", ["Panier moyen 12h", "Panier moyen 19h", "Panier moyen jour"])
        fig = px.histogram(df, x=selected_panier, title=f"Distribution : {selected_panier}")
        st.plotly_chart(fig)

    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    st.subheader("Analyse des Jours Fériés")
    ferie_df = df.groupby("Féries").agg({"Nbr total couv.": "mean", "Total additions": "mean", "Panier moyen jour": "mean"}).reset_index()
    ferie_df["Féries"] = ferie_df["Féries"].map({0: "Jour normal", 1: "Jour férié"})
    plot_grouped_bar(ferie_df, "Féries", ["Nbr total couv.", "Total additions", "Panier moyen jour"], "Impact des jours fériés",
                     {"Nbr total couv.": "Moyenne des couverts", "Total additions": "Additions moyennes", "Panier moyen jour": "Panier moyen"})

    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    st.subheader("Analyse journalière")

    # Convertir la colonne 'date' en datetime
    graph_df = df.copy()
    graph_df['Date'] = pd.to_datetime(graph_df['Date'])

    col1_graph9, col2_graph10 = st.columns(2)

    with col1_graph9:
        st.markdown(f'<p class="period-text">Couverts</p>' , \
            unsafe_allow_html=True)

        col1_filter1, col2_filter1, col3_filter1 = st.columns(3)

        with col1_filter1:
            group_by_option = st.selectbox('Trier par :', [
                    'Jour',
                    'Mois et Jour'], key='group_by_option1')

        with col2_filter1:
            data_type_option = st.selectbox('Sélectionnez le filtre :', [
                    'Nbr total couv. 12h',
                    'Nbr total couv. 19h',
                    'Nbr total couv.'
                    ], key='data_type_option1')

        if group_by_option == 'Mois et Jour':
            unique_months = graph_df['Date'].dt.to_period("M").unique() \
                .strftime('%m/%Y').tolist()
            with col3_filter1:
                month_option = st.selectbox('Sélectionnez le mois :', unique_months)

        else:
            month_option = None

        # Afficher le graphique en fonction des widgets
        show_grouped_data(group_by_option, data_type_option, group_by_option, \
            data_type_option, month_option, graph_df)

    with col2_graph10:
        st.markdown(f'<p class="period-text">Additions</p>' , \
            unsafe_allow_html=True)

        col1_filter2, col2_filter2, col3_filter2 = st.columns(3)
        with col1_filter2:
            group_by_option2 = st.selectbox('Trier par :', [
                    'Jour',
                    'Mois et Jour'], key='group_by_option2')
        with col2_filter2:
            data_type_option2 = st.selectbox('Sélectionnez le filtre :', [
                    'Additions 12h',
                    'Additions 19h',
                    'Total additions'
                    ], key='data_type_option2')

        if group_by_option2 == 'Mois et Jour':
            unique_months = graph_df['Date'].dt.to_period("M").unique() \
                .strftime('%m/%Y').tolist()
            with col3_filter2:
                month_option2 = st.selectbox('Sélectionnez le mois :', unique_months)

        else:
            month_option2 = None

        # Afficher le graphique en fonction des widgets
        show_grouped_data(group_by_option2, data_type_option2, group_by_option2, \
            data_type_option2, month_option2, graph_df)





if __name__ == "__main__":
    main()
