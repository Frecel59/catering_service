# Importation des bibliothèques nécessaires
import streamlit as st

# Utilisation de toute la largeur de l'écran
st.set_page_config(
    page_title="Pasino / Restauration",
    page_icon="img/logo_pasino.png",
    layout="wide"
)

# Pages avec leurs icônes respectives
pages = {
    "Informations": "📋",
    "Exports": "📤",
    "Analyses": "🔍",
    "Dashboard": "📊",
    "Analyses N-1": "📅",
    "Prédiction": "🔮"
}

# Liste des catégories
categories = {
    "Informations": ["Informations"],
    "Transmettre vos fichiers": ["Exports"],
    "Couverts": ["Analyses", "Dashboard", "Analyses N-1"],
    "Ventes": ["Analyses Ventes"]
}

def display_app_content():
    # Logo du Pasino
    st.sidebar.image('img/logo_pasino.png')

    # Utiliser une variable de session pour stocker la dernière page
    # Par défaut, aucune page sélectionnée
    selected_page = st.session_state.get("selected_page", "Informations")

    # Afficher le menu
    st.sidebar.title("Restauration")

    for category, pages_list in categories.items():
        st.sidebar.markdown(f"## {category}")
        for page in pages_list:
            if st.sidebar.button(page, key=page):
                selected_page = page

    # Mettre à jour la variable de session
    st.session_state.selected_page = selected_page

    # Afficher la page sélectionnée
    if selected_page == "Informations":
        import infos
        infos.main()
    elif selected_page == "Exports":
        import exports
        exports.main()
    elif selected_page == "Analyses":
        import analyses
        analyses.main()
    elif selected_page == "Analyses N-1":
        import analyses_n1
        analyses_n1.main()
    elif selected_page == "Prédiction":
        import predictions
        predictions.main()
    elif selected_page == "Dashboard":
        import dashboard
        dashboard.main()

    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    # Logo du Partouche
    st.sidebar.image('img/logo_p_partouche.png', width=30)

# ...
