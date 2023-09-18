# Importation des bibliothèques nécessaires
import streamlit as st

def main():
    # Utiliser une variable de session pour stocker la dernière page
    # Par défaut, aucune page sélectionnée
    selected_page = st.session_state.get("selected_page", None)

    # Si la variable de session est vide (première visite), ou si l'utilisateur
    # n'a pas sélectionné "Exports", définissez-la sur "Exports"
    if selected_page is None or selected_page != "Informations":
        selected_page = "Informations"

    # Afficher le menu
    st.sidebar.title("Menu")
    selected_page = st.sidebar.radio("Sélectionnez une page", [
        "Informations",
        "Exports",
        "Analyses",
        "Analyses N-1",
        "Prédiction"],
        index=["Informations",
               "Exports",
               "Analyses",
               "Analyses N-1",
               "Prédiction"].index(selected_page))

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



if __name__ == "__main__":
    main()
