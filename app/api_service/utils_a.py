def prepareJsonResponse(document: dict) -> dict:
    _id = document.pop("_id", None)
    timestamp = document.pop("timestamp", None)
    if _id:
        document["id"] = str(_id)
    if timestamp:
        document["timestamp"] = str(timestamp)
    return document
