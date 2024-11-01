import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SESSION_TYPE = 'filesystem'
    PASSWORD = "1234"  # Set the password here
