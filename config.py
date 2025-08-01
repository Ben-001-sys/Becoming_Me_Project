import os

class Config:
    # Flask session secret key
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Database connection string
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    # Disable tracking modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False
