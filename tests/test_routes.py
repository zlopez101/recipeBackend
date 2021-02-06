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
    _id = Deleted.pop("id")

    # delete the last recipe
    response = test_client.delete("/recipe/" + _id)
    assert response.status_code == 204

    # add the recipe back
    response = test_client.post("/recipes", data=Deleted)
    assert response.status_code == 201

    # make sure the recipe was added back
    response = test_client.get("/recipes")
    assert b"party size spanakopita melt" in response.data
    assert b"1/2 cup fresh cilantro, chopped, plus more for serving" in response.data
    assert b"https://www.halfbakedharvest.com/buffalo-chicken-pizza/" in response.data

    DELETED = {
        "userId": "5febad07b771396bbea8d358",
        "url": "https://www.halfbakedharvest.com/buffalo-chicken-pizza/",
        "name": "sheet pan buffalo chicken pizza",
        "source": "HalfBakedHarvest",
        "ingredients": [
            "1/2 pound pizza dough, homemade or store-bought",
            "1 cup cooked shredded chicken",
            "1/2 cup buffalo sauce (homemade sauce in notes)",
            "2 tablespoons chopped fresh chives",
            "2 teaspoons dried parsley",
            "1 teaspoon dried dill",
            "1/2 cup fresh cilantro or parsley, chopped",
            "1-2 cloves garlic, grated",
            "1/2-1 teaspoon fennel seeds",
            "1 pinch red pepper flakes",
            "1/3 cup ranch dressing (homemade sauce in notes)",
            "1/4 cup crumbled blue cheese (optional)",
            "1 cup shredded whole milk mozzarella",
            "1 cup shredded cheddar cheese",
            "1/2 cup grated parmesan or asiago cheese",
        ],
    }

