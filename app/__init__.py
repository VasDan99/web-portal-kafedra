from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return '<h1>Портал кафедры информационных систем</h1><p>Flask работает!</p>'

    return app