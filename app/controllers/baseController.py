class baseController:

    attributes = []

    def __init__(self, starter):
        for attribute in self.attributes:
            self.__setattr__(attribute, starter[attribute])

    @staticmethod
    def processResponse(document: dict) -> dict:
        """Object Id must be string-ified for json serializable
    
        :param response: mongodb response
        :type response: dict
        :return: json-ready dict
        :rtype: dict
        """
        if document:
            document["id"] = str(document.pop("_id", None))
            return document
        else:
            raise LookupError("Your query did not have any matching documents")
