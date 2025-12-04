import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey123')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # Render передаст URL базы
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
