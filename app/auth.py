from flask import request, abort
from functools import wraps
from app.controllers import UserController, RecipeController


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected",
            },
            401,
        )

    parts = auth.split(" ")

    if parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must start with: Bearer",
            },
            401,
        )
    elif len(parts) == 1:
        raise AuthError(
            {"code": "invalid_header", "description": "Token not found"}, 401
        )
    elif len(parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must be Bearer <token>",
            },
            401,
        )

    token = parts[1]
    return token


def user_auth_required(func):
    @wraps(func)
    def route_wrapper(*args, **kwargs):
        token = get_token_auth_header()
        user = UserController.getFromToken(token)
        return func(user, *args, **kwargs)

    return route_wrapper


def recipe_auth_required(func):
    @wraps(func)
    def route_wrapper(*args, **kwargs):
        token = get_token_auth_header()
        user = UserController.getFromToken(token)
        return func(RecipeController(user.id, user.active), *args, **kwargs)

    return route_wrapper
