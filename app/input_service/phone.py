from flask import Blueprint, request, redirect, url_for
from app.db import pymongo
from app.utils import getRecipe
from twilio.twiml.messaging_response import MessagingResponse

phone = Blueprint("phone", __name__)


@phone.route("/msg", methods=["GET", "POST"])
def receiveMsg():
    """Receive the url link from the client and add file to recipe Database"""
    _from = request.values.get("From")
    msg = request.values.get("Body", None)

    User = pymongo.db.users.find_one(dict(phone_number=_from))
    if not User:
        return redirect(url_for(".sendMessage"))
    userId = str(User["_id"])

    # is it a url
    if msg.startswith("http"):
        recipeInfo = getRecipe(msg, userId)
        pymongo.db.recipes.insert_one(recipeInfo)
        return f"{recipeInfo['name']}was added to your recipes!"

    # recipe requests
    else:
        response = MessagingResponse()
        response.message("What do you want?")
        return str(response)


@phone.route("/new_user")
def sendMessage():
    """Send the sign up link to the requestor"""
    response = MessagingResponse()
    response.message(
        f"Hello! Looks like you are a new user, please use the link to sign up for our service. Thanks!"
    )
    return str(response)


@phone.route("/createRecipe")
def create():
    """[summary]

    :return: [description]
    :rtype: [type]
    """
    return "hello world"


@phone.route("/addrecipe/")
def addrecipe():
    """Add a recipe to user's list

    :param userId: userId retrieve from user phone number
    :type userId: str
    :param url: url sent by user
    :type url: str
    """

    recipeInfo = getRecipe(url, userId)
    # return redirect(url_for("api_service.RecipeList"))s
    pymongo.db.recipes.insert_one(recipeInfo)
    return "hello"

