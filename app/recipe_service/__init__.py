from app.auth import *
from app.controllers.recipe import RecipeController
from app.utils import getRecipe, validate_json
from bson import ObjectId
from flask import Blueprint, jsonify, request
from flask.views import MethodView

from .utils_a import makePrediction

recipeService = Blueprint("recipe_service", __name__)


class RecipeAPI(MethodView):
    def auth_status(func):
        """Works active status to make sure each user identified 

        :param func: [description]
        :type func: [type]
        """

        def inner_func(*args, **kwargs):

            # can't directly reference the controller
            # index args to controller then check the .active attribute
            if args[1].active:
                return func(*args, **kwargs)
            else:
                return jsonify({"message": "invalid token"})

        return inner_func

    @auth_status
    def get(self, controller, recipeId):

        if recipeId is None:
            # return a list of recipes
            return jsonify(controller.getRecipes())
        else:
            # expose a single recipe
            return controller.getRecipe(recipeId)

    @auth_status
    def post(
        self, controller,
    ):
        # create a new recipe
        recipeURL = request.get_json()["url"]
        recipe = getRecipe(recipeURL, controller.userId)
        return controller.createRecipe(recipe)

    @auth_status
    def delete(self, controller, recipeId):
        # delete a single recipe
        controller.deleteRecipe(recipeId)
        return "deleted"

    @auth_status
    def put(self, controller, recipeId):
        # update a single recipe
        pass


@recipeService.route("/api/groceryList", methods=["POST"])
@user_auth_required
def groceryList(userId):
    ingredients = request.get_json()["ingredients"]
    preds = makePrediction([ingredient["ingredient"] for ingredient in ingredients])
    dct = {}
    labels = set(preds)
    for label in labels:
        dct[label] = []
    for ingredient, pred in zip(ingredients, preds):
        dct[pred].append(ingredient)
    return dct


recipe_view = recipe_auth_required(RecipeAPI.as_view("recipes"))
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
