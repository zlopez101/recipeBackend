import pytest
from tests.modelTesting import *
from app.controllers import RecipeController, UserController


def test_Recipes(models):
    first, second, third = Recipes()
    controller = RecipeController("602b77e223b58c90325936d8")
    # create a recipe, then retrieve it using the id
    first_id = controller.createRecipe(first)
    recipe = controller.getRecipe(first_id)
    assert (
        recipe["name"]
        == "25 Minute Korean Bulgogi BBQ Chicken with Spicy Garlic Butter Corn. "
    )
    controller.deleteRecipe(first_id)

    # get all the recipes under the fake userId 12334678
    recipes = controller.getRecipes()
    assert len(recipes) == 0, "No more recipes since we deleted the first inserted one"

    for recipe in Recipes():
        controller.createRecipe(recipe)

    recipes = controller.getRecipes()
    assert len(recipes) == 3, "All 3 recipes are in the database"


def test_Users(models):
    Jim, Kim = Users()

    # register Jim
    jimInDB = UserController.createFromRegistration(Jim)
    updatedJim = jimInDB.set(test=True)

    jim = UserController.getFromId(jimInDB.id)
    assert isinstance(jim, UserController)
    assert str(jim) == "Jim Bob"
    # check all the attributes
    assert jim.email == Jim["email"]
    assert jim.phone_number == Jim["phone_number"]
    assert jim.password != Jim["password"]
    assert jim.test == True
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
    kim = UserController.getFromId(kimInDB.id)
    assert isinstance(kim, UserController)
    assert str(kim) == "Kim Sue"
