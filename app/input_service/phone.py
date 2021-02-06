from flask import Blueprint, request, redirect, url_for
from app.db import pymongo
from .utils_i import getRecipe
from twilio.twiml.messaging_response import MessagingResponse

phone = Blueprint("phone", __name__)


@phone.route("/msg", methods=["GET", "POST"])
def receiveMsg():
    """Receive the url link from the client and add file to recipe Database"""
    _from = request.values.get("From")
    msg = request.values.get("Body", None)

    userId = str(pymongo.db.users.find_one(dict(phone_number=_from))._id)
    if not User:
        redirect(url_for("sendMessage", _from=_from))

    # is it a url
    if msg.startswith("http"):
        return redirect(url_for(".addRecipe", userId=userId, url=msg, _from=_from))

    # recipe requests


@phone.route("/new_user")
def sendMessage():
    """Send the sign up link to the requestor"""
    response = MessagingResponse()
    response.message(b)
    pass


@phone.route("/addRecipe/<userId>")
def addRecipe(userId: str, url: str) -> MessagingResponse:
    """Add a recipe to user's list

    :param userId: userId retrieve from user phone number
    :type userId: str
    :param url: url sent by user
    :type url: str
    :return: Message for twilio to respond with
    :rtype: MessagingResponse
    """
    recipeInfo = getRecipe(url, userId)
    pymongo.db.recipes.insert_one(recipeInfo)
    response = MessagingResponse()
    response.message(body="This is the message")
