import streamlit as st
import pandas as pd

def main():
    # Utiliser une variable de session pour stocker la dernière page sélectionnée
    selected_page = st.session_state.get("selected_page", "Analyses")

    # Afficher le menu
    st.sidebar.title("Menu")
    selected_page = st.sidebar.radio("Sélectionnez une page", ["Exports", "Analyses", "Prédiction"], index=["Exports", "Analyses", "Prédiction"].index(selected_page))

    # Mettre à jour la variable de session
    st.session_state.selected_page = selected_page

    # Afficher la page sélectionnée
    if selected_page == "Exports":
        import exports
        exports.main()
    elif selected_page == "Analyses":
        import analyses
        analyses.main()
    elif selected_page == "Prédiction":
        import predictions
        predictions.main()

if __name__ == "__main__":
    main()
