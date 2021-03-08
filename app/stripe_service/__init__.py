from flask import Blueprint, jsonify, current_app, request
from .utils import *
from ..utils import validate_json
from functools import wraps
import stripe

stripe_service = Blueprint("stripe_service", __name__)


@stripe_service.route("/checkout-session", methods=["GET"])
def get_checkout_session():
    stripe.api_key = current_app.config["STRIPE_API_KEY"]
    id = request.args.get("sessionId")
    checkout_session = stripe.checkout.Session.retrieve(id)
    return jsonify(checkout_session)


@stripe_service.route("/customer-portal", methods=["POST"])
def customer_portal():
    stripe.api_key = current_app.config["STRIPE_API_KEY"]
    data = json.loads(request.data)
    # For demonstration purposes, we're using the Checkout session to retrieve the customer ID.
    # Typically this is stored alongside the authenticated user in your database.
    checkout_session_id = data["sessionId"]
    checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

    # This is the URL to which the customer will be redirected after they are
    # done managing their billing with the portal.
    return_url = os.getenv("DOMAIN")

    session = stripe.billing_portal.Session.create(
        customer=checkout_session.customer, return_url=return_url
    )
    return jsonify({"url": session.url})


@stripe_service.route("/webhook", methods=["POST"])
def webhook_receieved():
    """Webhooks for various Stripe event
    Events to monitor:
    checkout.session.completed	    Sent when a customer clicks the Pay or Subscribe button in Checkout, informing you of a new purchase.
    invoice.paid	                Sent each billing interval when a payment succeeds.
    invoice.payment_failed	        Sent each billing interval if there is an issue with your customer’s payment method.

    Total Events that are being sent:
    setup_intent.succeeed
    setup_intent.created
    checkout.session.completed
    customer.created
    payment_method.attached
    invoice.created
    customer.subscription.created
    invoice.updated
    invoice.updated
    invoice.finalized
    customer.subscription.updated
    invoice.paid
    invoice.payment_succeeded
    """

    stripe.api_key = current_app.config["STRIPE_API_KEY"]
    event = None
    try:
        event = request.get_json()
    except:
        print("⚠️  Webhook error while parsing basic request." + str(e))
        return jsonify(success=False)

    # Handle the event
    if event and event["type"] == "checkout.session.completed":
        if handleCheckoutSessionCompleted(event):
            return jsonify(success=True)

    elif event and event["type"] == "invoice.paid":
        if handleInvoicePaid(event):
            return jsonify(success=True)

    elif event and event["type"] == "invoice.payment_failed":
        if handleInvoicePaymentFailed(event):
            return jsonify(success=True)

    else:
        # Unexpected event type
        print("Unhandled event type {}".format(event["type"]))

    return jsonify(success=True)
