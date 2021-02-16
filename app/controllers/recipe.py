from .baseController import baseController


class Recipe(baseController):

    attributes = ["id", "ingredients", "name", "source", "url", "userId"]

    def __init__(self, kwargs):
        super().__init__(kwargs)

    def __repr__(self):
        return f"Recipe(ID: {self.id}, {self.name})"

    def __str__(self):
        return self.name


class RecipeController:
    @staticmethod
    def getRecipe(_id: str) -> dict:
        """Get a single recipe

        :param _id: _id provided by frontend
        :type _id: str
        :return: dict with dict.keys(["id", "ingredients", "name", "source", "url", "userId"])
        :rtype: dict
        """
        return processResponse(
            app.db.pymongo.db.recipes.find_one({"_id": ObjectId(_id)})
        )

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
        result = [processResponse(recipe) for recipe in recipes]
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
