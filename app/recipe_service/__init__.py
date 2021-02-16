from flask import Blueprint, request, jsonify

# from flask_restful import Api, Resource, reqparse, abort
import json
from app.controllers.recipe import RecipeController

# from app.models import RecipeController
from bson import ObjectId
from .utils_a import makePrediction
from app.utils import getRecipe
from app.auth import auth_required

recipeService = Blueprint("recipe_service", __name__)


@recipeService.route("/api/recipe/<recipeId>", methods=["GET", "PUT", "DELETE"])
@auth_required
def recipe(token, recipeId):
    """[summary]

    :param recipeId: [description]
    :type recipeId: [type]
    :return: [description]
    :rtype: [type]
    """

    if request.method == "GET":
        return RecipeController.getRecipe(recipeId)

    if request.method == "PUT":
        return "PUT"
    if request.method == "DELETE":
        RecipeController.deleteRecipe(recipeId)
        return "DELETE"


@recipeService.route("/api/recipes", methods=["GET", "POST"])
@auth_required
def recipes(userId):

    if request.method == "GET":
        return jsonify(RecipeController.getRecipes(userId))

    if request.method == "POST":
        recipeURL = request.get_json()["url"]
        recipe = getRecipe(recipeURL, userId)
        return RecipeController.createRecipe(recipe)


@recipeService.route("/api/groceryList", methods=["POST"])
@auth_required
def groceryList(userId):

    ingredients = request.get_json(["ingredients"])
    preds = makePrediction([item["ingredient"] for item in ingredients])
    dct = {}
    labels = set(preds)
    for label in labels:
        dct[label] = []
    for ingredient, pred in zip(ingredients, preds):
        dct[pred].append(ingredient)
    return dct


# class Recipe(Resource):
#     """Get a specific recipe provided by _id parameter"""

#     def get(self, _id):
#         return RecipeController.getRecipe(_id)
#         # recipe = pymongo.db.recipes.find_one_or_404({"_id": ObjectId(_id)})
#         # return jsonify(prepareJsonResponse(recipe))

#     def delete(self, _id):
#         RecipeController.deleteRecipe(_id)
#         # deleted = pymongo.db.recipes.delete_one({"_id": ObjectId(_id)})

#         # return "", 204


# class GroceryList(Resource):
#     """Recieve a post request from the frontend, and respond with the sorted grocery list"""

#     def post(self):
#         ingredients = json.loads(request.data)["ingredients"]
#         preds = makePrediction([item["ingredient"] for item in ingredients])
#         dct = {}
#         labels = set(preds)
#         for label in labels:
#             dct[label] = []
#         for ingredient, pred in zip(ingredients, preds):
#             dct[pred].append(ingredient)
#         return dct


# class RecipeList(Resource):
#     """Get all the recipes for the user, or allow the user to create a new recipe"""

#     def get(self):
#         """Get all the recipes for the user

#         :return: list of recipe objects( dict with keys of ['id', 'ingredients', 'name', 'source', 'url', 'userId'])
#         :rtype: list
#         """
#         # user = pymongo.db.users.find_one({"_id": ObjectId("5febad07b771396bbea8d358")})
#         # recipes = pymongo.db.recipes.find({"userId": "5febad07b771396bbea8d358"})

#         # return jsonify([prepareJsonResponse(recipe) for recipe in recipes])

#         return jsonify(RecipeController.getRecipes("5febad07b771396bbea8d358"))

#     def post(self):
#         """Create a recipe for the user

#         :return: new recipe id
#         :rtype: str
#         """

#         recipeURL = json.loads(request.data).get("url")

#         if not recipeURL:
#             return "Please supply a recipe url"
#         recipe = getRecipe(recipeURL, "5febad07b771396bbea8d358")
#         # newRecipe = pymongo.db.recipes.insert_one(recipe)
#         # return str(newRecipe.inserted_id)
#         return RecipeController.createRecipe(recipe)


# api.add_resource(Recipe, "/api/recipe/<_id>")
# api.add_resource(RecipeList, "/api/recipes")
# api.add_resource(GroceryList, "/api/groceryList")
