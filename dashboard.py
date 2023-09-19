# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Importation des fonctions personnalisées depuis d'autres fichiers Python
from gcp import get_storage_client

def get_df_from_gcp():
    client, bucket = get_storage_client()
    blob_path = "COVERS_BRASSERIE_DF_FINALE/df_finale.xlsx"
    blob = bucket.blob(blob_path)
    in_memory_file = io.BytesIO()
    blob.download_to_file(in_memory_file)
    in_memory_file.seek(0)
    df = pd.read_excel(in_memory_file)
    return df

def main():
    st.title("Tableau de bord - Restauration")

    # Récupérer les données
    df = get_df_from_gcp()

    # Analyse Temporelle
    st.subheader("Analyse Temporelle")
    fig1 = px.line(df, x="Date", y=["Nbr total couv. 19h", "Nbr total couv. 12h"], title='Évolution des couverts au fil du temps')
    st.plotly_chart(fig1)

    # Répartition Jours/Fériés
    st.subheader("Répartition Jours/Fériés")
    fig2 = px.histogram(df, x="Jour", y="Nbr total couv.", color="Féries", title='Distribution du nombre de couverts par jour de la semaine')
    st.plotly_chart(fig2)

    # Analyse Météo
    st.subheader("Analyse Météo")
    fig3 = px.box(df, x="Météo 12h", y="Nbr total couv. 12h", title='Distribution des couverts de 12h selon la météo')
    st.plotly_chart(fig3)

    fig4 = px.box(df, x="Méteo 19h", y="Nbr total couv. 19h", title='Distribution des couverts de 19h selon la météo')
    st.plotly_chart(fig4)

    # Analyse des Serveurs
    st.subheader("Analyse des Serveurs")
    fig5 = px.scatter(df, x="Nbr serveurs 12h", y="Nbr total couv. 12h", title='Nombre de serveurs 12h vs Nombre total couv. 12h')
    st.plotly_chart(fig5)

    fig6 = px.scatter(df, x="Nbr serveurs 19h", y="Nbr total couv. 19h", title='Nombre de serveurs 19h vs Nombre total couv. 19h')
    st.plotly_chart(fig6)

    # Indicateurs Clés
    st.subheader("Indicateurs Clés")
    total_couv = df["Nbr total couv."].sum()
    mean_couv = df["Nbr total couv."].mean()
    median_couv = df["Nbr total couv."].median()
    st.write(f"Total couv.: {total_couv}")
    st.write(f"Moyenne couv.: {mean_couv:.2f}")
    st.write(f"Médiane couv.: {median_couv:.2f}")

    # Filtres
    st.subheader("Filtres")
    jour_filter = st.selectbox("Choisir le jour:", df["Jour"].unique())
    filtered_data = df[df["Jour"] == jour_filter]
    st.write(filtered_data)

if __name__ == "__main__":
    main()
