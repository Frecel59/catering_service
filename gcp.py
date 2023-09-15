from google.cloud import storage
from google.oauth2 import service_account
import os
from dotenv import load_dotenv

load_dotenv()

def get_storage_client():
    # Connexion avec GCP
    bucket_name = os.getenv('BUCKET_NAME')
    credentials_dict = {
        "type": os.getenv('TYPE'),
        "project_id": os.getenv('PROJECT_ID'),
        "private_key_id": os.getenv('PRIVATE_KEY_ID'),
        "private_key": os.getenv('PRIVATE_KEY').replace('\\n', '\n'),
        "client_email": os.getenv('CLIENT_EMAIL'),
        "client_id": os.getenv('CLIENT_ID'),
        "auth_uri": os.getenv('AUTH_URI'),
        "token_uri": os.getenv('TOKEN_URI'),
        "auth_provider_x509_cert_url": os.getenv('AUTH_PROVIDER_X509_CERT_URL'),
        "client_x509_cert_url": os.getenv('CLIENT_X509_CERT_URL')
    }

    # Créez des informations d'identification d'objet de compte de service à partir du dictionnaire
    credentials = service_account.Credentials.from_service_account_info(info=credentials_dict)

    # Créez un client Storage et retournez-le
    client = storage.Client(credentials=credentials)
    bucket = client.get_bucket(bucket_name)

    return client, bucket
