from functools import wraps
from flask import request, abort


def validate_json(*expectedArgs):
    def acceptRoute(func):
        @wraps(func)
        def wrapper_validate_json(*args, **kwargs):
            jsonObject = request.get_json()
            for expected_arg in expectedArgs:
                if expected_arg not in jsonObject:
                    abort(400)
            return func(*args, **kwargs)

        return wrapper_validate_json

    return acceptRoute

