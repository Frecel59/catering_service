import streamlit as st
import footer
import pandas as pd
import matplotlib.pyplot as plt

from utils import display_icon

def main():
    # Charger le contenu du fichier CSS
    with open('style.css', 'r') as css_file:
        css = css_file.read()

    # Afficher le contenu CSS dans la page Streamlit
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    #########################################################################
    #########################################################################

    # Afficher l'icône pour la page avec le titre personnalisé
    display_icon("Prédiction", "Prédiction du nombre de serveurs")

    # Afficher le message "Développement en cours"
    st.markdown(
        """
        <div style="text-align:center;">
            <h2 style="color:red;">🚧 Développement en cours 🚧</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    #########################################################################
    ############################## EN COURS #################################
    #########################################################################

def display_statistics(df):
    st.title("Rapport Statistique Complet")

    # 1. Analyse des couverts
    st.subheader("1. Analyse des couverts")

    # Total des couverts par jour
    st.markdown("### Total des couverts par jour")
    df.groupby('Jour')['Nbr total couv. 19h', 'Nbr total couv. 12h'].sum().plot(kind='bar')
    st.pyplot(plt.gcf())
    plt.clf()

    # Répartition des couverts offerts vs payants
    st.markdown("### Répartition des couverts offerts vs payants")
    df[['Nbr couv. off 19h', 'Nbr couv. off 12h']].sum().plot(kind='pie')
    st.pyplot(plt.gcf())
    plt.clf()

    # Tendance des couverts au fil du temps
    st.markdown("### Tendance des couverts au fil du temps")
    df.set_index('Date')[['Nbr total couv. 19h', 'Nbr total couv. 12h']].plot()
    st.pyplot(plt.gcf())
    plt.clf()

    # 2. Analyse des additions
    st.subheader("2. Analyse des additions")

    # Total des additions par jour
    st.markdown("### Total des additions par jour")
    df.groupby('Jour')['Total additions'].sum().plot(kind='bar')
    st.pyplot(plt.gcf())
    plt.clf()

    # Répartition des additions pour les couverts offerts vs payants
    st.markdown("### Répartition des additions pour les couverts offerts vs payants")
    df[['Additions off 19h', 'Additions off 12h']].sum().plot(kind='pie')
    st.pyplot(plt.gcf())
    plt.clf()

    # Tendance des additions au fil du temps
    st.markdown("### Tendance des additions au fil du temps")
    df.set_index('Date')['Total additions'].plot()
    st.pyplot(plt.gcf())
    plt.clf()

    # 3. Analyse de la météo
    st.subheader("3. Analyse de la météo")

    # Influence de la météo sur le nombre de couverts
    st.markdown("### Influence de la météo sur le nombre de couverts")
    df.groupby('Météo 12h')['Nbr total couv. 12h'].mean().plot(kind='bar')
    st.pyplot(plt.gcf())
    plt.clf()

    # Influence de la météo sur les additions
    st.markdown("### Influence de la météo sur les additions")
    df.groupby('Météo 12h')['Total additions'].mean().plot(kind='bar')
    st.pyplot(plt.gcf())
    plt.clf()

    # 4. Performance des serveurs
    st.subheader("4. Performance des serveurs")

    # Nombre de serveurs par jour
    st.markdown("### Nombre de serveurs par jour")
    df.groupby('Jour')['Nbr total serveurs'].mean().plot(kind='bar')
    st.pyplot(plt.gcf())
    plt.clf()

    # Panier moyen par serveur
    st.markdown("### Panier moyen par serveur")
    df['Panier moyen total'] = df['Total additions'] / df['Nbr total couv.']
    df[['Panier moyen total', 'Panier moyen 12h', 'Panier moyen 19h']].mean().plot(kind='bar')
    st.pyplot(plt.gcf())
    plt.clf()

    st.markdown("<hr/>", unsafe_allow_html=True)



    footer.display()

if __name__ == "__main__":
    main()
