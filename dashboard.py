# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import io

# Importation des fonctions personnalisées depuis d'autres fichiers Python
from gcp import get_storage_client

# Fonction pour formater une date en français
def format_date_in_french(date):
    # Liste des noms de mois en français
    mois = [
        'janvier',
        'février',
        'mars',
        'avril',
        'mai',
        'juin',
        'juillet',
        'août',
        'septembre',
        'octobre',
        'novembre',
        'décembre']

    # Formater la date au format "jour mois année"
    return f"{date.day} {mois[date.month - 1]} {date.year}"

# Fonction principale
def get_df_from_gcp():
    # Charger le contenu du fichier CSS
    with open('style.css', 'r') as css_file:
        css = css_file.read()

    # Afficher le contenu CSS dans la page Streamlit
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    #########################################################################
    #########################################################################

    # Afficher l'icône pour la page avec le titre personnalisé
    # display_icon("Analyses", "Analyses d'une période")

    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    #########################################################################
    ############# CHAMPS INPUT POUR LE CHOIX DE LA PERIODE ##################
    #########################################################################
    # Début de la section pour le bilan en fonction des jours et services

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

    # Appeler la fonction get_df_from_gcp pour obtenir les données
    df_final = get_df_from_gcp()

    st.markdown(f'<p class="period-text">Choississez une période</p>' , \
        unsafe_allow_html=True)

    # Créer une mise en page en colonnes
    col1, col2 = st.columns(2)

    # Ajouter le widget date_input dans la première colonne
    with col1:
        start_date = st.date_input("Date de départ", \
            datetime((df_final["Date"].max()).year - 1, 11, 1), \
            key="start_date_input", format="DD/MM/YYYY")
            # 01/11 + année -1 de date max
        formatted_start_date = format_date_in_french(start_date)

    with col2:
        end_date = st.date_input("Date de fin", df_final["Date"].max(), \
            key="end_date_input", format="DD/MM/YYYY")
        formatted_end_date = format_date_in_french(end_date)

    # Convertir les dates sélectionnées en objets datetime64[ns]
    start_date_convert = pd.to_datetime(start_date)
    end_date_convert = pd.to_datetime(end_date)

    # Filtrer le DataFrame en fonction des dates choisies
    filtered_df = df_final[(df_final["Date"] >= start_date_convert) & \
        (df_final["Date"] <= end_date_convert)]

    return filtered_df

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
