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

    # ======================================================
    # НАСТРОЙКИ ДЛЯ ОТПРАВКИ EMAIL
    # ======================================================
    
    # ВЫБЕРИТЕ ОДИН ИЗ ТРЁХ ВАРИАНТОВ:
    
    # ---- Вариант 1: Mail.ru ----
    MAIL_SERVER = 'smtp.mail.ru'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'your_email@mail.ru'
    MAIL_PASSWORD = 'your_app_password'
    MAIL_DEFAULT_SENDER = 'your_email@mail.ru'
    
    # ---- Вариант 2: Яндекс (Yandex) ----
    # MAIL_SERVER = 'smtp.yandex.ru'
    # MAIL_PORT = 465
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    # MAIL_USERNAME = 'your_email@yandex.ru'
    # MAIL_PASSWORD = 'your_app_password'
    # MAIL_DEFAULT_SENDER = 'your_email@yandex.ru'
    
    # ---- Вариант 3: Gmail ----
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = False
    # MAIL_USERNAME = 'your_email@gmail.com'
    # MAIL_PASSWORD = 'your_app_password'
    # MAIL_DEFAULT_SENDER = 'your_email@gmail.com'

# Для отладки — выводим путь (только для Timeweb)
if os.environ.get('TIMEWEB_CLOUD'):
    print(f"Database path: {db_path}")
    print(f"Exists: {os.path.exists(db_path)}")