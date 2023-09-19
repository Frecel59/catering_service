import streamlit as st

def display_icon(page_name):
    icons = {
        "Informations": "📋",
        "Exports": "📤",
        "Analyses": "🔍",
        "Analyses N-1": "📅",
        "Prédiction": "🔮"
    }
    if page_name in icons:
        st.markdown(f"<h1 style='text-align: left;'>{icons[page_name]}</h1>", unsafe_allow_html=True)
