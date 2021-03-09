from .baseController import baseController
from bson import ObjectId
import app.db


class RecipeController(baseController):
    def __init__(self, userId: str, active: bool):
        self.userId = userId
        self.active = active
        self.db = app.db.pymongo.db.recipes

    def response_headers(self):
        pass

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

    def getRecipe(self, _id: str) -> dict:
        """Get a single recipe

        :param _id: _id provided by frontend
        :type _id: str
        :return: dict with dict.keys(["id", "ingredients", "name", "source", "url", "userId"])
        :rtype: dict
        """
        result = baseController.processResponse(
            self.db.find_one({"_id": ObjectId(_id)})
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

    def getRecipes(self) -> list:
        """Get all recipes

        :return: list of recipe objects 
        :rtype: list
        """
        recipes = self.db.find({"userId": self.userId})

        result = [self.processResponse(recipe) for recipe in recipes]
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

    def deleteRecipe(self, _id: str) -> None:
        """Deletes recipes

        :param _id: id provided by frontend
        :type _id: str
        """
        self.db.delete_one({"_id": ObjectId(_id)})
        return None

    def createRecipe(self, recipe: dict) -> str:
        """create a new recipe

        :param recipe: dict created from `getRecipe`
        :type recipe: dict
        :return: ID of newly created recipe
        :rtype: str
        """
        recipe["userId"] = self.userId
        newRecipe = self.db.insert_one(recipe)
        return str(newRecipe.inserted_id)
