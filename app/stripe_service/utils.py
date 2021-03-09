from ..controllers import UserController


def handleCheckoutSessionCompleted(event: dict) -> bool:
    """handle the checkout.session.completed event received from stripe webhook
    
    The customer document in MongoDB should have status updated to active.
    The userController.createTimer() method should be called 

    :param event: JSON from stripe
    :type event: dict   
    :return: True if handled successfully
    :rtype: bool
    """
    print("handling checkout.session.completed...")
    try:
        user = UserController.getFromId(event["data"]["object"]["client_reference_id"])
        user.createTimer()
        user.set(active=True)
        return True
    # client_reference_id was not properly set...
    except KeyError as e:
        return False
    except Exception as e:
        print(f"There was an error: \n{e}")


def handleInvoicePaid(event: dict) -> bool:
    """handle the invoice.paid event

    The userController.createTimer() method should be called so that token timer is replaced with the new value
    
    :param event: JSON from stripe
    :type event: dict
    :return: True if handled successfully
    :rtype: bool
    """
    print(f"handling invoice.paid event...")
    return True


def handleInvoicePaymentFailed(event: dict) -> bool:
    """handle the invoice.payment_failed event

    :param event: JSON from stripe
    :type event: dict
    :return: True if handled successfully
    :rtype: bool
    """
    print("handling invoice.payment_failed event...")
    return True
