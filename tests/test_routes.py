import pytest
import json
from tests.modelTesting import *
from app.auth import AuthError


def test_recipe_routes(test_client):
    """[summary]"""

    # set up
    Jim, Kim = Users()
    recipes = Recipes()
    headers = {"content-type": "application/json"}

    # register the user
    clientId = test_client.post("/api/register", headers=headers, json=Jim)

    # login the user
    apiCall = {"email": Jim["email"], "password": Jim["password"]}
    token = test_client.post("/api/login", headers=headers, json=apiCall)

    # update the headers to add the authorization
    headers["Authorization"] = f"Bearer {token.data.decode('utf-8')}"

    # create recipe
    apiCall = {"url": recipes[0]["url"]}
    firstRecipeId = test_client.post("/api/recipes", headers=headers, json=apiCall)

    # check the recipe list
    JimsRecipes = test_client.get("/api/recipes", headers=headers)

    assert (
        b"25 Minute Korean Bulgogi BBQ Chicken with Spicy Garlic Butter Corn. "
        in JimsRecipes.data
    ), "proper recipe needed to be added"
    assert firstRecipeId.data in JimsRecipes.data, "Recipe should the same ID"

    # add another recipe to client (Jim)'s list
    apiCall = {"url": recipes[1]["url"]}
    secondRecipeId = test_client.post("/api/recipes", headers=headers, json=apiCall)

    # check the recipe list again
    # this time, convert to json to make sure recipes are different
    JimsRecipes = json.loads(test_client.get("/api/recipes", headers=headers).data)
    assert len(JimsRecipes) == 2, "We have added 2 of 3 rbecipes"

    first, second = JimsRecipes
    assert first["name"] == recipes[0]["name"], "Not doing a full comparsion"
    secondIngredients = [
        ingredient["ingredient"] for ingredient in second["ingredients"]
    ]
    assert (
        secondIngredients == recipes[1]["ingredients"]
    ), "Since API adds userId and id"
    assert first["userId"] == second["userId"], "userId should match"

    # register a second user
    headers = {"content-type": "application/json"}  # overwrite
    clientId = test_client.post("/api/register", headers=headers, json=Kim)

    # login the user
    apiCall = {"email": Kim["email"], "password": Kim["password"]}
    token = test_client.post("/api/login", headers=headers, json=apiCall)

    # update the headers
    headers["Authorization"] = f"Bearer {token.data.decode('utf-8')}"

    # Kim tries to add a recipe to her list
    apiCall = {"url": recipes[-1]["url"]}
    thirdRecipeId = test_client.post("/api/recipes", headers=headers, json=apiCall)

    # check her recipes list
    KimsRecipes = test_client.get("/api/recipes", headers=headers)
    assert (
        thirdRecipeId.data in KimsRecipes.data
    ), "Kim's recipe id should be in her recipes"
    assert (
        secondRecipeId.data not in KimsRecipes.data
    ), "Jim's recipes should not be there"
    KimsRecipes = json.loads(KimsRecipes.data)

    assert len(KimsRecipes) == 1, "There is only 1 recipe in her list"

    # try to get a single recipe for kim
    recipe = test_client.get(
        "/api/recipes/" + thirdRecipeId.data.decode("utf-8"), headers=headers
    )
    # assert recipes[-1]["name"] == json.loads(recipe.data)["name"]

    # try to delete kim's recipe
    _ = test_client.delete(
        "/api/recipes/" + thirdRecipeId.data.decode("utf-8"), headers=headers
    )
    # now test her recipe list
    KimsRecipes = json.loads(test_client.get("/api/recipes", headers=headers).data)
    assert len(KimsRecipes) == 0, "there are no more recipes in her list"


def test_user_routes(test_client):
    Jim, Kim = Users()
    headers = {"content-type": "application/json"}
    # test a working user
    response = test_client.post("/api/register", json=Jim, headers=headers)
    assert response.status_code == 200
    # test registration that doesn't have all required information
    jim_missing_data = Jim.copy()
    jim_missing_data.pop("email")
    response = test_client.post("/api/register", json=jim_missing_data, headers=headers)
    assert response.status_code == 400

    # try to login
    jimsAPICall = {"email": Jim["email"], "password": Jim["password"]}
    response = test_client.post("/api/login", headers=headers, json=jimsAPICall,)
    assert response.status_code == 200
    token = response.data.decode("utf-8")

    response = test_client.post(
        "/api/logout", headers={"Authorization": f"Bearer {token}"}
    )
