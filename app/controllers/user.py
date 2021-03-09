from app import bcrypt
from bson import ObjectId
import app.db
import jwt
from datetime import datetime, timedelta
from .baseController import baseController
import os


class UserController(baseController):
    key = os.environ.get("FLASK_APP_BUILDING_KEY")

    def __init__(self, kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

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
        """creates the User object from token. Used after token validation

        :param token: str of userId decoded from token
        :type token: str
        :return: Instance of UserController
        :rtype: UserController
        """
        user = UserController.get({"_id": ObjectId(_id)})
        return cls(user)

    @classmethod
    def getFromToken(cls, token: str):
        """creates the User object from token. Used after token validation

        :param token: str of userId decoded from token
        :type token: str
        :return: Instance of UserController
        :rtype: UserController
        """
        try:
            payload = jwt.decode(token, UserController.key, algorithms="HS256")
            _id = payload.get("userID")
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."

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
        """register a new user. Creates a new field with {"active": False}

        :param userObj: dict with keys from Vue frontend
        :type userObj: dict
        :return: UserController instance
        :rtype: UserController
        """
        user = userObj.copy()
        user["password"] = bcrypt.generate_password_hash(user.pop("password"))

        # if active is already defined, for the testing
        if user.get("active"):
            pass
        else:
            # set equal to True when the event checkout.session.completed
            user["active"] = False

        app.db.pymongo.db.users.insert_one(user)
        return cls(UserController.processResponse(user))

    @classmethod
    def createFromStripe(cls, stripeId: str):
        """create the user

        :param stripeId: stripe id returned from the event webhook
        :type stripeId: string
        :return: UserController instance   
        :rtype: UserController
        """
        user = UserController.get({"stripe_customer_id": stripeId})
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

    def createTimer(self, timer: int = 31):
        """create a timer token that can be decoded within timer days

        :param timer: Amount of days for the timer to active, defaults to 31
        :type timer: int, optional
        """
        payload = {
            "exp": datetime.utcnow() + timedelta(days=timer),
            "iat": datetime.utcnow(),
            "userID": self.id,
        }
        token = jwt.encode(payload, UserController.key, algorithm="HS256")
        self.set(timerToken=token)

    def set(self, **kwargs):
        """Update the UserController Instance to include"""
        dct = {"users." + key: value for key, value in kwargs.items()}
        return app.db.pymongo.db.users.update_one(
            {"_id": ObjectId(self.id)}, {"$set": kwargs}
        )

