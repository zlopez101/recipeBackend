from flask import Blueprint, request, redirect, url_for
from bson import ObjectId
from app.controllers.user import UserController
import json
from app.utils import validate_json

from app.auth import auth_required

userService = Blueprint("user_service", __name__)


@userService.route("/api/register", methods=["POST"])
@validate_json("email", "password", "fname", "lname", "phone_number")
def register():
    user = UserController.createFromRegistration(request.get_json())
    return user.encodeToken()


@userService.route("/api/login", methods=["POST"])
@validate_json("email", "password")
def login():
    user = UserController.fromLogin(request.get_json())
    return user.encodeToken()


@userService.route("/api/logout", methods=["POST"])
@auth_required
def logout(userId):
    # print(userId)
    user = UserController.getFromId(userId)
    return f"{user} signed out!"


@userService.route("/api/account")
def account():
    pass


@userService.route("/api/settings")
def settings():
    pass

