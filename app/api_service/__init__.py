from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse, abort
import json
from app.db import pymongo
from bson import ObjectId
from .utils_a import prepareJsonResponse, makePrediction

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
        ingredients = request.values.get("ingredients")
        if not (ingredients):
            return 400
        preds = makePrediction(ingredients)
        results = list(zip(ingredients, preds))
        return jsonify(results), 201


class RecipeList(Resource):
    """Get all the recipes for the user, or allow the user to create a new recipe"""

    def get(self):
        user = pymongo.db.users.find_one({"_id": ObjectId("5febad07b771396bbea8d358")})
        recipes = pymongo.db.recipes.find({"userId": "5febad07b771396bbea8d358"})

        return jsonify([prepareJsonResponse(recipe) for recipe in recipes])

    def post(self):
        # DELETED = {
        #     "userId": "5febad07b771396bbea8d358",
        #     "url": "https://www.halfbakedharvest.com/buffalo-chicken-pizza/",
        #     "name": "sheet pan buffalo chicken pizza",
        #     "source": "HalfBakedHarvest",
        #     "ingredients": [
        #         "1/2 pound pizza dough, homemade or store-bought",
        #         "1 cup cooked shredded chicken",
        #         "1/2 cup buffalo sauce (homemade sauce in notes)",
        #         "2 tablespoons chopped fresh chives",
        #         "2 teaspoons dried parsley",
        #         "1 teaspoon dried dill",
        #         "1/2 cup fresh cilantro or parsley, chopped",
        #         "1-2 cloves garlic, grated",
        #         "1/2-1 teaspoon fennel seeds",
        #         "1 pinch red pepper flakes",
        #         "1/3 cup ranch dressing (homemade sauce in notes)",
        #         "1/4 cup crumbled blue cheese (optional)",
        #         "1 cup shredded whole milk mozzarella",
        #         "1 cup shredded cheddar cheese",
        #         "1/2 cup grated parmesan or asiago cheese",
        #     ],
        # }
        newRecipe = dict(request.values)
        newRecipe = pymongo.db.recipes.insert_one(newRecipe)
        return str(newRecipe.inserted_id), 201


api.add_resource(Recipe, "/recipe/<_id>")
api.add_resource(RecipeList, "/recipes")
