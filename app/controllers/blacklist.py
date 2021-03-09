from .baseController import baseController
from datetime import datetime
import app.db


class BlackListToken:

    # figure out how to schedule jobs to invalidate tokens tbd

    def __init__(self, token):
        self.token = token
        self.db = app.db.pymongo.db.blacklist
        self.on_blacklist = self.performCheck()

    def performCheck(self) -> bool:
        if not (self.db.find_one({"token": self.token})):
            return True
        else:
            return False

    def addToDB(self):
        self.db.insert_one({"token": self.token, "insertedAt": datetime.utcnow()})

    def __eq__(self, other):
        """comparison of tokens

        :param other: token to compare
        :type other: BlackListToken
        """
        assert isinstance(
            other, BlackListToken
        ), "Comparison must be made between BlackListToken. {b} is not member of class"
        if self.token == other.token:
            return True
        else:
            return False

    def __repr__(self):
        return f"BlackListToken({self.token})"
