import pytest
import json


def test_recipe_routes(test_client):
    """[summary]"""

    # get a single recipe
    response = test_client.get("/recipe/601c2d83a418aff42b7fa72e")
    assert b"party size spanakopita melt" in response.data

    # get all the recipes
    response = test_client.get("/recipes")
    assert b"party size spanakopita melt" in response.data
    assert b"1/2 cup fresh cilantro, chopped, plus more for serving" in response.data
    assert b"https://www.halfbakedharvest.com/buffalo-chicken-pizza/" in response.data
    recipes = json.loads(response.data)
    Deleted = recipes[-1]
    print(Deleted)
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

