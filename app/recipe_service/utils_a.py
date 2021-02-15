from joblib import load
from sys import platform


def makePrediction(ingredients: list) -> list:
    """Use the model generated to make predictions on the list

    :param ingredients: ingredients list
    :type ingredients: list
    :return: list of predictions indexed to ingredients list
    :rtype: list
    """
    if platform == "win32":
        model_filename = r"app\recipe_service\model.joblib"
    else:
        model_filename = "app/recipe_service/model.joblib"
    model = load(model_filename)
    return model.predict(ingredients)
