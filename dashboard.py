import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import io
from gcp import get_storage_client
from utils import display_icon


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

    st.subheader("Analyse des Jours Fériés")
    ferie_df = df.groupby("Féries").agg({"Nbr total couv.": "mean", "Total additions": "mean", "Panier moyen jour": "mean"}).reset_index()
    ferie_df["Féries"] = ferie_df["Féries"].map({0: "Jour normal", 1: "Jour férié"})
    plot_grouped_bar(ferie_df, "Féries", ["Nbr total couv.", "Total additions", "Panier moyen jour"], "Impact des jours fériés",
                     {"Nbr total couv.": "Moyenne des couverts", "Total additions": "Additions moyennes", "Panier moyen jour": "Panier moyen"})

    st.subheader("Analyse de la Météo")
    plot_grouped_bar(df.groupby("Météo 12h").mean().reset_index(), "Météo 12h", ["Nbr total couv. 12h", "Total additions"], "Impact de la météo sur les couverts et additions",
                    {"Nbr total couv. 12h": "Moyenne des couverts à 12h", "Total additions": "Additions moyennes"})

    st.subheader("Distribution des Couverts")
    fig = px.histogram(df, x="Nbr total couv.", title="Distribution du nombre total de couverts")
    st.plotly_chart(fig)

    st.subheader("Corrélations")
    corr = df[["Nbr total couv.", "Total additions", "Temp. 12h", "Nbr total serveurs"]].corr()
    fig = px.imshow(corr, title="Matrice de corrélation")
    st.plotly_chart(fig)

    st.subheader("Indicateurs Clés")
    total_couv = df["Nbr total couv."].sum()
    mean_couv = df["Nbr total couv."].mean()
    median_couv = df["Nbr total couv."].median()
    st.write(f"Total couv.: {total_couv}")
    st.write(f"Moyenne couv.: {mean_couv:.2f}")
    st.write(f"Médiane couv.: {median_couv:.2f}")

    st.subheader("Filtres")
    jour_filter = st.selectbox("Choisir le jour:", df["Jour"].unique())
    st.write(df[df["Jour"] == jour_filter])


if __name__ == "__main__":
    main()
