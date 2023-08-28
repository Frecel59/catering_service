import streamlit as st

def main():
    st.sidebar.title("Menu")
    selected_page = st.sidebar.radio("Sélectionnez une page", ["Exports", "Analyses", "Prédiction"])

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
