import pytest
import json
from tests.modelTesting import *
from app.auth import AuthError


def test_recipe_routes(test_client):
    """[summary]"""

    # create 3 recipes
    response = test_client.post(
        "/api/recipes",
        data=json.dumps({"url": "https://www.halfbakedharvest.com/spanakopita-melt/"}),
    )
    # response.data
    # get a single recipe
    # response = test_client.get("/api/recipe/601c2d83a418aff42b7fa72e")
    # assert b"party size spanakopita melt" in response.data

    # get all the recipes
    response = test_client.get("/api/recipes")
    assert b"12-16 ounces fresh baby spinach" in response.data
    # assert b"1/2 cup fresh cilantro, chopped, plus more for serving" in response.data
    # assert b"https://www.halfbakedharvest.com/buffalo-chicken-pizza/" in response.data
    # recipes = json.loads(response.data)
    # Deleted = recipes[-1]pass
    # print(Deleted)
    # _id = Deleted.pop("id")

    # delete the last recipe
    # response = test_client.delete("/recipe/" + _id)
    # assert response.status_code == 204

    # add the recipe back
    # response = test_client.post("/recipes", data=Deleted)
    # assert response.status_code == 201

    # make sure the recipe was added back
    # response = test_client.get("/recipes")
    # assert b"party size spanakopita melt" in response.data
    # assert b"1/2 cup fresh cilantro, chopped, plus more for serving" in response.data
    # assert b"https://www.halfbakedharvest.com/buffalo-chicken-pizza/" in response.data


def test_user_routes(test_client):
    Jim, Kim = Users()
    # test a working user
    response = test_client.post(
        "/register", json=Jim, headers={"content-type": "application/json"}
    )
    assert response.status_code == 200
    # test registration that doesn't have all required information
    jim_missing_data = Jim.copy()
    jim_missing_data.pop("email")
    response = test_client.post(
        "/register", data=jim_missing_data, headers={"content-type": "application/json"}
    )
    assert response.status_code == 400

