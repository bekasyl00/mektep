import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://mektep_user:password123@localhost/mektep_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads")
