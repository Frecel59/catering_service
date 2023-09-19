# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Importation des fonctions personnalisées depuis d'autres fichiers Python
from gcp import get_storage_client

def get_df_from_gcp():
        client, bucket = get_storage_client()

        # Chemin vers votre fichier dans le bucket
        blob_path = "COVERS_BRASSERIE_DF_FINALE/df_finale.xlsx"
        blob = bucket.blob(blob_path)

        # Téléchargez le fichier dans un objet en mémoire
        in_memory_file = io.BytesIO()
        blob.download_to_file(in_memory_file)
        in_memory_file.seek(0)

        # Lisez le fichier Excel dans un DataFrame
        df = pd.read_excel(in_memory_file)

        return df

def main():
    st.title("Tableau de bord - Restauration")

    # Récupérer les données
    df = get_df_from_gcp()

    # Sidebar
    date = st.sidebar.multiselect(
        "Sélectionnez une Date",
        options=df["Date"].unique(),
        default=df["Date"].unique(),
    )
    jour = st.sidebar.multiselect(
        "Sélectionnez un Jour",
        options=df["Jour"].unique(),
        default=df["Jour"].unique(),
    )
    meteo_12h = st.sidebar.multiselect(
        "Sélectionnez la Météo à 12h",
        options=df["Météo 12h"].unique(),
        default=df["Météo 12h"].unique(),
    )

    df_selection = df[df['Date'].isin(date) & df['Jour'].isin(jour) & df['Météo 12h'].isin(meteo_12h)]

    # Afficher le DataFrame filtré
    with st.expander("Visualiser les Données"):
        st.dataframe(df_selection)

    # Créer un graphique simple (ajustez en fonction de vos besoins)
    fig = px.bar(df_selection, x="Jour", y="Nombre de clients", title="Nombre de clients par jour")
    st.plotly_chart(fig)



# Si ce fichier est exécuté directement, appelez la fonction main()
if __name__ == "__main__":
    main()
