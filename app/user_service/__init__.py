from flask import Blueprint, request, redirect, url_for, current_app, jsonify
from bson import ObjectId
from app.controllers import UserController, BlackListToken
import json
from app.utils import validate_json
import stripe

from app.auth import user_auth_required, get_token_auth_header

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
def logout():
    """Accept Vue Frontend token, add to mongodb blacklisted Collection

    :return: 201,
    :rtype: int
    """
    try:
        token = get_token_auth_header()
        blacklisted = BlackListToken(token)
        blacklisted.addToDB()
        return "added", 201
    except Exception as e:
        print(e)
        return "failed", 500


@userService.route("/api/account")
@user_auth_required
def account(user):
    pass


@userService.route("/api/settings")
@user_auth_required
def settings(user):
    pass


@userService.route("/api/billing")
@user_auth_required
def biling(user):
    stripe.api_key = current_app.config["STRIPE_API_KEY"]
    baseUrl = request.headers.get("referer", "https://localhost:5000/")
    try:
        session = stripe.billing_portal.Session.create(
            customer=user.stripe_customer_id, return_url=baseUrl + "account"
        )
        return jsonify({"url": session.url})
    except AttributeError as e:
        print(e)
        return jsonify({"url": "", "code": "error", "msg": "there was an error"})
    except stripe.error.InvalidRequestError as e:
        print(e)
        return jsonify({"url": "", "code": "error", "msg": "there was an error"})

