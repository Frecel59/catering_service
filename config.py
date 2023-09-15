import os



class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    BUCKET_NAME = os.getenv('BUCKET_NAME')
