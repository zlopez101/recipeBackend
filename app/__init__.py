from flask import Flask
from flask_cors import CORS
from app.config import Configuration
from app.db import pymongo


def create_app(config_class=Configuration):
    """Application Factory for the recipe app"""

    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(config_class)
    app.config["CORS_HEADERS"] = "Content-Type"
    pymongo.init_app(app)

    @app.route("/")
    def home():
        return "Hello World!"

    from app.api_service import apiService
    from app.input_service.phone import phone

    app.register_blueprint(apiService)
    app.register_blueprint(phone)
    return app
