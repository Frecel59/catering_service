from google.cloud import storage
from google.oauth2 import service_account
import os
from dotenv import load_dotenv

load_dotenv()

################# Connexion avec GCP ###########################################
# Récupérer le nom du bucket à partir de la variable d'environnement
bucket_name = os.getenv('BUCKET_NAME')

# Récupérer les informations d'identification du compte de service à partir du fichier JSON
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

# Créer des informations d'identification d'objet de compte de service à partir du dictionnaire
credentials = service_account.Credentials.from_service_account_info(info=credentials_dict)

# Créer un client Storage
client = storage.Client(credentials=credentials)

# Récupérer une référence à votre bucket GCP
bucket = client.get_bucket(bucket_name)
