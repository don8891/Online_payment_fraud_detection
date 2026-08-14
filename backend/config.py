import os

class Config:
    """
    Base configuration settings for the Flask backend application.
    """
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JSON_SORT_KEYS = False
