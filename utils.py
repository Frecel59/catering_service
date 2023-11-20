# utils.py

import streamlit as st

def display_icon(page_name, custom_title=None):
    icons = {
        "Informations": "📋",
        "Exports": "📤",
        "Bilan": "🔍",
        "Dashboard": "📊",
        "Analyses N-1": "📅",
        "Prédiction": "🔮"
    }
    if page_name in icons:
        display_title = custom_title if custom_title else page_name
        st.markdown(f"<h1 style='text-align: center;'>{icons[page_name]} {display_title}</h1>", unsafe_allow_html=True)
