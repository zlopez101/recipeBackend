from app import bcrypt
from bson import ObjectId
import app.db
import jwt
from datetime import datetime, timedelta
from .baseController import baseController
import os


class UserController(baseController):
    key = os.environ.get("FLASK_APP_BUILDING_KEY")
    attributes = ["fname", "lname", "email", "phone_number", "password", "id"]

    def __init__(self, kwargs):
        super().__init__(kwargs)

    def __repr__(self):
        return f"User({self._id})"

    def __str__(self):
        return f"{self.fname} {self.lname}"

    @staticmethod
    def find(parameters: dict) -> list:
        """returns cursor objec that must be iterated over

        :param parameters: dict with keys as query, values are objects to return that match
        :type parameters: dict
        :return: cursor (list) of documents
        :rtype: list
        """
        return app.db.pymongo.db.users.find(parameters)

    @classmethod
    def getFromId(cls, _id: str):
        """creates the User object from _id. Used after token validation

        :param _id: str of userId decoded from token
        :type _id: str
        :return: Instance of UserController
        :rtype: UserController
        """
        user = UserController.get({"_id": ObjectId(_id)})
        return cls(user)

    @classmethod
    def fromLogin(cls, suppliedUserData: dict):
        """login a user based on email/phone_number + password

        :param suppliedUserData: dict with keys(["email | phone_number", "password"])
        :type suppliedUserData: dict
        :return: UserController instance for 
        :rtype: UserController
        """
        user = UserController.get({"email": suppliedUserData.get("email")})
        if bcrypt.check_password_hash(user["password"], suppliedUserData["password"]):
            return cls(user)

    @classmethod
    def createFromRegistration(cls, userObj: dict):
        """register a new user

        :param userObj: dict with keys from Vue frontend
        :type userObj: dict
        :return: UserController instance
        :rtype: UserController
        """
        user = userObj.copy()
        user["password"] = bcrypt.generate_password_hash(user.pop("password"))
        app.db.pymongo.db.users.insert_one(user)
        return cls(UserController.processResponse(user))

    @staticmethod
    def get(data: dict) -> dict:
        """retrieve a user from database

        :return: user instance based on phone number
        :rtype: dict
        """
        return UserController.processResponse(app.db.pymongo.db.users.find_one(data))

    def encodeToken(self) -> bytes:
        """create a token to return to Vue Frontend

        :param userId: id of user
        :type userId: str
        :return: auth token as bytes
        :rtype: bytes
        """
        payload = {
            "exp": datetime.utcnow() + timedelta(days=1),
            "iat": datetime.utcnow(),
            "userID": self.id,
        }
        return jwt.encode(payload, UserController.key, algorithm="HS256")

    @staticmethod
    def decodeToken(token: str) -> str:
        """decode a provided token

        :param token: token from Vue Frontend
        :type token: str
        :return: ID of user
        :rtype: str
        """
        try:
            payload = jwt.decode(token, UserController.key, algorithms="HS256")
            return payload.get("userID")
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."
