import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'your-secret-key-here'
    
    # Абсолютный путь для Timeweb Cloud
    db_path = os.path.join(basedir, 'instance', 'portal.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BABEL_DEFAULT_LOCALE = 'ru'
    LANGUAGES = ['ru', 'en', 'zh']

    
# Для отладки — выводим путь (только для Timeweb)
if os.environ.get('TIMEWEB_CLOUD'):
    print(f"Database path: {db_path}")
    print(f"Exists: {os.path.exists(db_path)}")