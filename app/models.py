import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from bson import ObjectId
from app import bcrypt
import app.db


def processResponse(document: dict) -> dict:
    """Object Id must be string-ified for json serializable

    :param response: mongodb response
    :type response: dict
    :return: json-ready dict
    :rtype: dict
    """
    document["id"] = str(document.pop("_id", None))
    return document


class RecipeController:
    @staticmethod
    def getRecipe(_id: str) -> dict:
        """Get a single recipe

        :param _id: _id provided by frontend
        :type _id: str
        :return: dict with dict.keys(["id", "ingredients", "name", "source", "url", "userId"])
        :rtype: dict
        """
        return processResponse(
            app.db.pymongo.db.recipes.find_one({"_id": ObjectId(_id)})
        )

    @staticmethod
    def getRecipes(userId) -> list:
        """Get all recipes

        :return: list of recipe objects 
        :rtype: list
        """
        # user = app.db.pymongo.db.users.find_one(
        # {"_id": ObjectId("5febad07b771396bbea8d358")}
        # )
        recipes = app.db.pymongo.db.recipes.find({"userId": userId})
        result = [processResponse(recipe) for recipe in recipes]
        return result

    @staticmethod
    def deleteRecipe(_id: str) -> None:
        """Deletes recipes

        :param _id: id provided by frontend
        :type _id: str
        """
        app.db.pymongo.db.recipes.delete_one({"_id": ObjectId(_id)})
        return None

    @staticmethod
    def createRecipe(recipe: dict) -> str:
        """create a new recipe

        :param recipe: dict created from `getRecipe`
        :type recipe: dict
        :return: ID of newly created recipe
        :rtype: str
        """
        newRecipe = app.db.pymongo.db.recipes.insert_one(recipe)
        return str(newRecipe.inserted_id)


class User:

    key = os.environ.get("FLASK_APP_BUILDING_KEY")

    @classmethod
    def fromMongo(cls):
        pass

    def fromFrontend(cls):
        pass

    @staticmethod
    def login(suppliedUserData: dict) -> str:
        """login a user based on email/phone_number + password

        :param suppliedUserData: dict with keys(["email | phone_number", "password"])
        :type suppliedUserData: dict
        :return: token supplied by `User.encodeToken` method
        :rtype: str
        """
        user = User.getUser({"email": suppliedUserData.get("email")})
        if bcrypt.check_password_hash(user["password"], suppliedUserData["password"]):
            return User.encodeToken(user["id"])

    @staticmethod
    def createUser(userObj: dict) -> str:
        """register a new user

        :param userObj: dict with keys from Vue frontend
        :type userObj: dict
        :return: id of created user     
        :rtype: str
        """
        user = userObj.copy()
        user["password"] = bcrypt.generate_password_hash(user.pop("password"))
        newUser = app.db.pymongo.db.users.insert_one(user)
        return str(newUser.inserted_id)

    @staticmethod
    def getUser(data: dict) -> dict:
        """retrieve a user from database

        :return: user instance based on phone number
        :rtype: dict
        """
        return processResponse(app.db.pymongo.db.users.find_one(data))

    @staticmethod
    def encodeToken(userId: str) -> bytes:
        """create a token to return to Vue Frontend

        :param userId: id of user
        :type userId: str
        :return: auth token as bytes
        :rtype: bytes
        """
        payload = {
            "exp": datetime.utcnow() + timedelta(days=1),
            "iat": datetime.utcnow(),
            "userID": userId,
        }
        return jwt.encode(payload, User.key, algorithm="HS256")

    @staticmethod
    def decodeToken(token: str) -> str:
        """decode a provided token

        :param token: token from Vue Frontend
        :type token: str
        :return: ID of user
        :rtype: str
        """
        try:
            payload = jwt.decode(token, User.key, algorithms="HS256")
            return payload.get("userID")
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."
