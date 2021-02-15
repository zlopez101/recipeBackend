from flask import Blueprint, request, redirect, url_for
from app.models import User
import json
from .utils import validate_json

# from app.auth import auth_required

userService = Blueprint("user_service", __name__)


@validate_json("email", "password", "fname", "lname", "phone_number")
@userService.route("/register", methods=["GET", "POST"])
def register():
    userData = request.get_json()
    print(userData)
    return User.createUser(userData)


@validate_json("email", "password")
@userService.route("/login")
def login():
    return User.login(request.get_json())


@userService.route("/logout")
def logout():
    pass


@userService.route("/account")
def account():
    pass


@userService.route("/settings")
def settings():
    pass

