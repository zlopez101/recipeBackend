from flask import Blueprint, request, jsonify
from flask.views import MethodView

# from flask_restful import Api, Resource, reqparse, abort
import json
from app.controllers.recipe import RecipeController

# from app.models import RecipeController
from bson import ObjectId
from .utils_a import makePrediction
from app.utils import getRecipe
from app.auth import auth_required

recipeService = Blueprint("recipe_service", __name__)


class RecipeAPI(MethodView):
    def get(self, userId, recipeId):
        if recipeId is None:
            # return a list of recipes
            return jsonify(RecipeController.getRecipes(userId))
        else:
            # expose a single recipe
            return RecipeController.getRecipe(recipeId)

    def post(
        self, userId,
    ):
        # create a new recipe
        recipeURL = request.get_json()["url"]
        recipe = getRecipe(recipeURL, userId)
        return RecipeController.createRecipe(recipe)

    def delete(self, userId, recipeId):
        # delete a single recipe
        RecipeController.deleteRecipe(recipeId)
        return "deleted"

    def put(self, userId, recipeId):
        # update a single recipe
        pass


recipe_view = auth_required(RecipeAPI.as_view("recipes"))
recipeService.add_url_rule(
    "/api/recipes",
    defaults={"recipeId": None},
    view_func=recipe_view,
    methods=["GET",],
)
recipeService.add_url_rule("/api/recipes", view_func=recipe_view, methods=["POST",])
recipeService.add_url_rule(
    "/api/recipes/<recipeId>", view_func=recipe_view, methods=["GET", "PUT", "DELETE"]
)
