from flask import Flask
from flask_cors import CORS
from app.config import Configuration
from app.db import pymongo


def create_app(config_class=Configuration):
    """Application Factory for the recipe app"""

    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)
    pymongo.init_app(app)

    from app.api_service import apiService
    from app.input_service.phone import phone

    app.register_blueprint(apiService)
    app.register_blueprint(phone)
    return app
