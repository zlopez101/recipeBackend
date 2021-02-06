import os

mongo_pass = os.environ.get("MONGO_DB")


class Configuration:

    SECRET_KEY = os.urandom(32)
    MONGO_URI = (
        "mongodb+srv://zach:"
        + mongo_pass
        + "@spacerepetitioncluster.3l5he.mongodb.net/recipeMaker?retryWrites=true&w=majority"
    )
    DEBUG = True
    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    TWILIO_TEST_ACCOUNT_SID = os.environ.get("TWILIO_TEST_ACCOUNT_SID")
    TWILIO_TEST_AUTH_TOKEN = os.environ.get("TWILIO_TEST_AUTH_TOKEN")


class TestingConfiguration:

    SECRET_KEY = os.urandom(32)
    MONGO_URI = (
        "mongodb+srv://zach:"
        + mongo_pass
        + "@spacerepetitioncluster.3l5he.mongodb.net/recipeMaker?retryWrites=true&w=majority"
    )
    TESTING = True
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    TWILIO_TEST_ACCOUNT_SID = os.environ.get("TWILIO_TEST_ACCOUNT_SID")
    TWILIO_TEST_AUTH_TOKEN = os.environ.get("TWILIO_TEST_AUTH_TOKEN")
