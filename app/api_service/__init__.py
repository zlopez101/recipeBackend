from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse, abort
import json
from app.db import pymongo
from bson import ObjectId
from .utils_a import prepareJsonResponse

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


class RecipeList(Resource):
    """Get all the recipes for the user, or allow the user to create a new recipe"""

    def get(self):
        user = pymongo.db.users.find_one({"_id": ObjectId("5febad07b771396bbea8d358")})
        recipes = pymongo.db.recipes.find({"userId": "5febad07b771396bbea8d358"})

        return jsonify([prepareJsonResponse(recipe) for recipe in recipes])

    def post(self):
        newRecipe = dict(request.values)
        newRecipe = pymongo.db.recipes.insert_one(newRecipe)
        return str(newRecipe.inserted_id), 201


api.add_resource(Recipe, "/recipe/<_id>")
api.add_resource(RecipeList, "/recipes")
