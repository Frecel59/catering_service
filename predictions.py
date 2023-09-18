import streamlit as st
import footer

def main():
    # Charger le contenu du fichier CSS
    with open('style.css', 'r') as css_file:
        css = css_file.read()

    # Afficher le contenu CSS dans la page Streamlit
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    #########################################################################
    #########################################################################

    st.title("Prédictions")

    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    #########################################################################
    ############################## EN COURS #################################
    #########################################################################

    footer.display()

if __name__ == "__main__":
    main()
