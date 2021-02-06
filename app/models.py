class Recipe:
    """Helper for all the recipes
    """

    def __init__(self, *args):
        for arg in args:
            setattr(self, arg, arg)

    # def __init__(self, _id, userId, url, name, source, ingredients):
    #     self._id = _id
    #     self.userId = userId
    #     self.url = url
    #     self.name = name
    #     self.source = source
    #     self.ingredients = ingredients

    @classmethod
    def fromGetIngredient()

    @classmethod
    def fromDB(document):
        """create the Recipe Object from the document returned by the mongo_db

        :param document: [description]
        :type document: [type]
        :return: [description]
        :rtype: Recipe
        """
        return Recipe(
            str(document["_id"]),
            document["_id"],
            document["userId"],
            document["url"],
            document["name"],
            document["source"],
            document["ingredients"],
        )

    def toDB()