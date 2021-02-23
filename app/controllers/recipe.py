from .baseController import baseController
from bson import ObjectId
import app.db


class RecipeController(baseController):
    @staticmethod
    def createIngredientObj(recipe: dict) -> dict:
        """New method for storing inactive objects in the frontend will be in the store

        :param recipe: the result from database query
        :type recipe: dict
        :return: altered result with ingredients array of object ingredients
        :rtype: dict
        """
        ingredient = {"active": True, "from": recipe.get("name")}
        recipe["newIngredient"] = [
            ingredient.update({"ingredient": ingred})
            for ingred in recipe["ingredients"]
        ]
        return recipe

    @staticmethod
    def getRecipe(_id: str) -> dict:
        """Get a single recipe

        :param _id: _id provided by frontend
        :type _id: str
        :return: dict with dict.keys(["id", "ingredients", "name", "source", "url", "userId"])
        :rtype: dict
        """
        result = baseController.processResponse(
            app.db.pymongo.db.recipes.find_one({"_id": ObjectId(_id)})
        )

        result["newIngredients"] = []
        for index, ingredient in enumerate(result["ingredients"]):
            result["newIngredients"].append(
                {
                    "ingredient": ingredient,
                    "active": True,
                    "from": result["id"],
                    "id": index,
                }
            )
        result["ingredients"] = result.pop("newIngredients")
        return result

    @staticmethod
    def getRecipes(userId) -> list:
        """Get all recipes

        :return: list of recipe objects 
        :rtype: list
        """
        # user = app.db.pymongo.db.users.find_one(
        # {"_id": ObjectId("5febad07b771396bbea8d358")}
        # )
        recipes = app.db.pymongo.db.recipes.find({"userId": userId})

        result = [baseController.processResponse(recipe) for recipe in recipes]

        for recipe in result:
            recipe["newIngredients"] = []
            for index, ingredient in enumerate(recipe["ingredients"]):
                recipe["newIngredients"].append(
                    {
                        "ingredient": ingredient,
                        "active": True,
                        "from": recipe["id"],
                        "id": recipe["id"] + " " + str(index),
                    }
                )
            recipe["ingredients"] = recipe.pop("newIngredients")
        return result

    @staticmethod
    def deleteRecipe(_id: str) -> None:
        """Deletes recipes

        :param _id: id provided by frontend
        :type _id: str
        """
        app.db.pymongo.db.recipes.delete_one({"_id": ObjectId(_id)})
        return None

    @staticmethod
    def createRecipe(recipe: dict) -> str:
        """create a new recipe

        :param recipe: dict created from `getRecipe`
        :type recipe: dict
        :return: ID of newly created recipe
        :rtype: str
        """
        newRecipe = app.db.pymongo.db.recipes.insert_one(recipe)
        return str(newRecipe.inserted_id)
