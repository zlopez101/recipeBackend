from flask import Blueprint, request, redirect, url_for, current_app, jsonify
from bson import ObjectId
from app.controllers.user import UserController
import json
from app.utils import validate_json
import stripe

from app.auth import user_auth_required

userService = Blueprint("user_service", __name__)


@userService.route("/api/register", methods=["POST"])
@validate_json("email", "password", "fname", "lname", "phone_number")
def register():
    stripe.api_key = current_app.config["STRIPE_API_KEY"]
    user = UserController.createFromRegistration(request.get_json())
    baseUrl = request.headers.get("referer", "https://localhost:5000/")
    try:
        checkout_session = stripe.checkout.Session.create(
            success_url=baseUrl + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=baseUrl + "failed",
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price": stripe.Price.list()["data"][0]["id"],
                    # For metered billing, do not pass quantity
                    "quantity": 1,
                }
            ],
            customer_email=user.email,
            client_reference_id=user.id,
            subscription_data={"trial_period_days": 30},
        )
        return jsonify(
            {
                "token": user.encodeToken().decode("utf-8"),
                "sessionId": checkout_session["id"],
                "pk": "pk_test_51I0Hi7AJqS6KUAStIg73brufDB8SmNTBqFvYFLyt7vAV1Ecbf7fPzDDIiwFflpnyD9tbYvaObpEpLhj9lBqROwZC00WywiUsQk",
            }
        )
    except Exception as e:
        print(e)
        return jsonify({"error": {"message": str(e)}}), 400


@userService.route("/api/login", methods=["POST"])
@validate_json("email", "password")
def login():
    user = UserController.fromLogin(request.get_json())
    return user.encodeToken()


@userService.route("/api/logout", methods=["POST"])
@user_auth_required
def logout(user):
    return f"{user.fname} {user.lname} signed out!"


@userService.route("/api/account")
@user_auth_required
def account():
    pass


@userService.route("/api/settings")
@user_auth_required
def settings():
    pass

