import streamlit as st

class Config:
    SECRET_KEY = st.secrets['SECRET_KEY']
    BUCKET_NAME = st.secrets['BUCKET_NAME']
