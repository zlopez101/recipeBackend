from joblib import load
from sys import platform


def prepareJsonResponse(document: dict) -> dict:
    _id = document.pop("_id", None)
    timestamp = document.pop("timestamp", None)
    if _id:
        document["id"] = str(_id)
    if timestamp:
        document["timestamp"] = str(timestamp)
    return document


def makePrediction(ingredients: list) -> list:
    """Use the model generated to make predictions on the list

    :param ingredients: ingredients list
    :type ingredients: list
    :return: list of predictions indexed to ingredients list
    :rtype: list
    """
    if platform == "win32":
        model_filename = r"app\api_service\model.joblib"
    else:
        model_filename = "app/api_service/model.joblib"
    model = load(model_filename)
    return model.predict(ingredients)
