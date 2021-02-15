import pytest
from app.models import *
from tests.modelTesting import *


def test_Recipes(models):
    first, second, third = Recipes()

    # create a recipe, then retrieve it using the id
    first_id = RecipeController.createRecipe(first)
    recipe = RecipeController.getRecipe(first_id)
    assert (
        recipe["name"]
        == "25 Minute Korean Bulgogi BBQ Chicken with Spicy Garlic Butter Corn. "
    )
    RecipeController.deleteRecipe(first_id)

    # get all the recipes under the fake userId 12334678
    recipes = RecipeController.getRecipes(12345678)
    assert len(recipes) == 0, "No more recipes since we deleted the first inserted one"

    for recipe in Recipes():
        RecipeController.createRecipe(recipe)

    recipes = RecipeController.getRecipes(12345678)
    assert len(recipes) == 3, "All 3 recipes are in the database"


def test_Users(models):
    Jim, Kim = Users()
    jim_id = User.createUser(Jim)
    # try to login Jim with password
    # correct password
    jimsAPICall = {"email": Jim["email"], "password": Jim["password"]}
    token = User.login(jimsAPICall)
    possibly_jims_id = User.decodeToken(token)

    assert jim_id == possibly_jims_id, "did we find the right id?"

    # try to login Jim with password

