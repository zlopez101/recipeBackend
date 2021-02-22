from flask import Flask, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from app.config import Configuration
import app.db

bcrypt = Bcrypt()


def create_app(config_class=Configuration):
    """Application Factory for the recipe app"""

    myapp = Flask(__name__)
    cors = CORS(myapp, resources={r"/api/*": {"origins": "*"}})
    myapp.config.from_object(config_class)
    myapp.config["CORS_HEADERS"] = "Content-Type"
    app.db.pymongo.init_app(myapp)

    @myapp.route("/")
    def home():
        return "Hello World!"

    # from app.auth import AuthError

    # @myapp.errorhandler(AuthError)
    # def handle_error(ex):
    #     response = jsonify(ex.error)
    #     response.status_code = ex.status_code
    #     return response

    from app.recipe_service import recipeService
    from app.input_service import inputService
    from app.user_service import userService

    myapp.register_blueprint(recipeService)
    myapp.register_blueprint(inputService)
    myapp.register_blueprint(userService)
    return myapp
