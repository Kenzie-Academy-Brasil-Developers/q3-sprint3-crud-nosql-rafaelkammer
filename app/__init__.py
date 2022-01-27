from flask import Flask

from app import routes

def create_app():

    app = Flask(__name__, static_folder=None)

    routes.init_app(app)

    return app