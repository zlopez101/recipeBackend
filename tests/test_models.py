import pytest
from app.models import *
from tests.modelTesting import *
from app.controllers.user import UserController


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
    jim_id = User.createFromRegistration(Jim)
    # try to login Jim with password
    # correct password
    jimsAPICall = {"email": Jim["email"], "password": Jim["password"]}
    token = User.login(jimsAPICall)
    possibly_jims_id = User.decodeToken(token)
    assert jim_id == possibly_jims_id, "did we find the right id?"

    # try to login Jim with password


def test_controller(models):
    Jim, Kim = Users()

    # register Jim
    jimInDB = UserController.createFromRegistration(Jim)

    # use the getFromId method
    jim = UserController.getFromId(jimInDB)
    assert isinstance(jim, UserController)
    assert str(jim) == "Jim Bob"

    # check all the attributes
    assert jim.email == Jim["email"]
    assert jim.phone_number == Jim["phone_number"]
    assert jim.password != Jim["password"]
    # use the login method
    jimsAPICall = {"email": Jim["email"], "password": Jim["password"]}
    jim = UserController.fromLogin(jimsAPICall)
    token = jim.encodeToken()
    # give the token back to the frontend
    # do some stuff
    # frontend submits a request to an auth_required route
    jim_id = UserController.decodeToken(token)
    assert jim.id == jim_id

    # register Kim
    kimInDB = UserController.createFromRegistration(Kim)

    # use the getFromId method
    kim = UserController.getFromId(kimInDB)
    assert isinstance(kim, UserController)
    assert str(kim) == "Kim Sue"
