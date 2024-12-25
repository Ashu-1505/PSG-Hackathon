import os

class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'secure_vault'
    SECRET_KEY = os.urandom(24)  # Flask session secret key
