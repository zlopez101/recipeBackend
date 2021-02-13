from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse, abort
import json
from app.db import pymongo
from bson import ObjectId
from .utils_a import prepareJsonResponse, makePrediction
from app.utils import getRecipe

apiService = Blueprint("api_service", __name__)
api = Api(apiService)


def abortIfRecipeDoesNotExist(_id: str):
    """if the recipe does not exist by that id, abort the request and return 404

    :param _id: id provided by requestor
    :type _id: str
    """
    pass


class Recipe(Resource):
    """Get a specific recipe provided by _id parameter"""

    def get(self, _id):
        recipe = pymongo.db.recipes.find_one_or_404({"_id": ObjectId(_id)})
        return jsonify(prepareJsonResponse(recipe))

    def delete(self, _id):
        deleted = pymongo.db.recipes.delete_one({"_id": ObjectId(_id)})
        return "", 204


class GroceryList(Resource):
    """Recieve a post request from the frontend, and respond with the sorted grocery list"""

    def post(self):
        ingredients = json.loads(request.data)["ingredients"]
        preds = makePrediction([item["ingredient"] for item in ingredients])
        dct = {}
        labels = set(preds)
        for label in labels:
            dct[label] = []
        for ingredient, pred in zip(ingredients, preds):
            dct[pred].append(ingredient)
        return dct


class RecipeList(Resource):
    """Get all the recipes for the user, or allow the user to create a new recipe"""

    def get(self):
        """Get all the recipes for the user

        :return: list of recipe objects( dict with keys of ['id', 'ingredients', 'name', 'source', 'url', 'userId'])
        :rtype: list
        """
        user = pymongo.db.users.find_one({"_id": ObjectId("5febad07b771396bbea8d358")})
        recipes = pymongo.db.recipes.find({"userId": "5febad07b771396bbea8d358"})

        return jsonify([prepareJsonResponse(recipe) for recipe in recipes])

    def post(self):
        """Create a recipe for the user

        :return: new recipe id
        :rtype: str
        """

        recipeURL = json.loads(request.data).get("url")

        if not recipeURL:
            return "Please supply a recipe url"
        recipe = getRecipe(recipeURL, "5febad07b771396bbea8d358")
        newRecipe = pymongo.db.recipes.insert_one(recipe)
        return str(newRecipe.inserted_id)


api.add_resource(Recipe, "/api/recipe/<_id>")
api.add_resource(RecipeList, "/api/recipes")
api.add_resource(GroceryList, "/api/groceryList")
