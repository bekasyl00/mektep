import os

class Config:
    # Секретный ключ для сессий и flash
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey123')

    # URL для подключения к PostgreSQL
    # Если на Render есть DATABASE_URL, он её использует, иначе дефолт
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres1:kBztkPjG32gKTCMfBvHwVTGTQ7Xms5Il@dpg-d4osgdc9c44c738fuod0-a/mektep_db_9ybu'
    )

    # Отключаем уведомления SQLAlchemy об изменениях
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Папка для загрузки фото учителей
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
