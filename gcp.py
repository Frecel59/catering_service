from google.cloud import storage
from google.oauth2 import service_account
import streamlit as st

def get_storage_client():
    # Connexion avec GCP
    bucket_name = st.secrets['BUCKET_NAME']
    credentials_dict = {
        "type": st.secrets['TYPE'],
        "project_id": st.secrets['PROJECT_ID'],
        "private_key_id": st.secrets['PRIVATE_KEY_ID'],
        "private_key": st.secrets['PRIVATE_KEY'].replace('\\n', '\n'),
        "client_email": st.secrets['CLIENT_EMAIL'],
        "client_id": st.secrets['CLIENT_ID'],
        "auth_uri": st.secrets['AUTH_URI'],
        "token_uri": st.secrets['TOKEN_URI'],
        "auth_provider_x509_cert_url": st.secrets['AUTH_PROVIDER_X509_CERT_URL'],
        "client_x509_cert_url": st.secrets['CLIENT_X509_CERT_URL']
    }

    # Créez des informations d'identification d'objet de compte de service à partir du dictionnaire
    credentials = service_account.Credentials.from_service_account_info(info=credentials_dict)

    # Créez un client Storage et retournez-le
    client = storage.Client(credentials=credentials)
    bucket = client.get_bucket(bucket_name)

    return client, bucket
