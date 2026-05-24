from flask import Flask
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route('/')git add .
git commit -m "Initial Flask app - portal работает"
git push
    def index():
        return "<h1>Портал кафедры информационных систем</h1><p>Flask работает!</p>"

    return app