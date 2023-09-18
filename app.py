# Importation des bibliothèques nécessaires
import streamlit as st

def display_app_content():
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

def main():
        # Charger le contenu du fichier CSS
    with open('style.css', 'r') as css_file:
        css = css_file.read()

    # Afficher le contenu CSS dans la page Streamlit
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


    # Vérifiez si l'utilisateur est déjà authentifié
    if st.session_state.get("authenticated", False):
        display_app_content()
    else:
        # Logo de l'entreprise
        st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhSUdVHlJsrGI4AIs3nUbSD-QPpnfiKOLVWw&usqp=CAU')
        st.title("Authentification")
        st.write("Veuillez entrer le mot de passe pour accéder à l'application.")

        # Demander le mot de passe à l'utilisateur
        pwd = st.text_input("Entrez le mot de passe :", type="password")
        if st.button("Se connecter"):
            stored_pwd = st.secrets["PASSWORD"]
            if pwd == stored_pwd:
                st.session_state.authenticated = True
                st.success("Vous êtes maintenant connecté!")
                display_app_content()  # Afficher le contenu de l'application
            else:
                st.error("Mot de passe incorrect.")

if __name__ == "__main__":
    main()
