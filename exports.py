import os
import io
import pandas as pd
import streamlit as st
from gcp import get_storage_client
from google.cloud.exceptions import NotFound
from google.cloud import storage
import footer

from Data_cleaning.df_global import merged_df
from Data_cleaning.df_global_ventes import merged_data_ventes
from utils import display_icon


def upload_to_bucket(file, folder_name):
    client, bucket = get_storage_client()

    # Construire le nom de fichier complet avec le préfixe du dossier.
    filename = os.path.join(folder_name, file.name)

    # Télécharge le fichier dans le bucket.
    blob = bucket.blob(filename)
    blob.upload_from_file(file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    print(f"File {file.name} uploaded to {filename}.")

# Utiliser le séparateur horizontal avec la classe CSS personnalisée
st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

def save_final_dataframe(df, export_name):
    # Initialisation de la barre de progression
    progress = st.progress(0)
    st.title(f"Sauvegarde des données pour l'export {export_name} en cours, merci de patienter...")

    progress.progress(25)

    # Convertir le DataFrame directement en un objet BytesIO pour éviter de le sauvegarder localement
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    progress.progress(50)

    # Créer un objet de fichier semblable avec le contenu du BytesIO et le nom souhaité
    final_file = type('', (object,), {'name': f'{export_name}_df_finale.xlsx', 'read': output.read, 'seek': output.seek, 'tell': output.tell})()

    progress.progress(75)

    # Réinitialisez la position à 0 pour être sûr
    final_file.seek(0)

    # Téléchargez ce "fichier" dans le bucket
    upload_to_bucket(final_file, "DF_FINALE")
    progress.progress(100)
    st.title(f"Sauvegarde des données pour l'export {export_name} terminée...")

def main():
    # Charger le contenu du fichier CSS
    with open('style.css', 'r') as css_file:
        css = css_file.read()

    # Afficher le contenu CSS dans la page Streamlit
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    #########################################################################
    #########################################################################

    # Afficher l'icône pour la page "Exports" avec le titre personnalisé
    display_icon("Exports", "Exportations des fichiers")

    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])

    with col2:
        st.markdown("***Fichiers concernant les couverts***")

        # Upload pour Brasserie
        brasserie_file = st.file_uploader("Choisissez un fichier ***Brasserie*** (.xlsx)", type=["xlsx"])
        if brasserie_file:
            upload_to_bucket(brasserie_file, "COVERS_BRASSERIE")
            brasserie_file = merged_df()
            save_final_dataframe(brasserie_file, "COVERS")

        # Upload pour Snack
        snack_file = st.file_uploader("Choisissez un fichier ***Snack*** (.xlsx)", type=["xlsx"])
        if snack_file:
            upload_to_bucket(snack_file, "COVERS_SNACK")
            snack_file = merged_df()
            save_final_dataframe(snack_file, "COVERS")

        # Utiliser le séparateur horizontal avec la classe CSS personnalisée
        st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

        st.markdown("***Fichiers concernant les ventes***")

        # Upload pour Vente Brasserie
        ventes_brasserie_file = st.file_uploader("Choisissez un fichier ***Ventes Brasserie*** (.xlsx)", type=["xlsx"])
        if ventes_brasserie_file:
            upload_to_bucket(ventes_brasserie_file, "VENTES_BRASSERIE")
            ventes_brasserie_file = merged_data_ventes()
            save_final_dataframe(ventes_brasserie_file, "VENTES")

        # Upload pour Vente Snack
        ventes_snack_file = st.file_uploader("Choisissez un fichier ***Ventes Snack*** (.xlsx)", type=["xlsx"])
        if ventes_snack_file:
            upload_to_bucket(ventes_snack_file, "VENTES_SNACK")
            # ventes_snack_file = merged_data_ventes()
            # save_final_dataframe(ventes_snack_file, "VENTES")


    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    footer.display()

if __name__ == "__main__":
    main()
