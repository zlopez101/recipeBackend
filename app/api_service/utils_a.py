from joblib import load


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
    model = load(r"app\api_service\model.joblib")
    return model.predict(ingredients)
