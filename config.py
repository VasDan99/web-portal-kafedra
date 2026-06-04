import os


class Config:
    SECRET_KEY = 'your-secret-key-here'
    # Для деплоя на Timeweb Cloud используем /tmp/portal.db
    # Локально можно оставить instance/portal.db
    if os.environ.get('DEPLOY_ENV') == 'production':
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/portal.db'
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance',
                                                              'portal.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BABEL_DEFAULT_LOCALE = 'ru'
    LANGUAGES = ['ru', 'en', 'zh']