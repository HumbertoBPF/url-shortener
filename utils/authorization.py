import jwt
from flask import request
from sqlalchemy import select

from database.config import db
from database.models import User
from settings import SECRET_JWT


def get_jwt_token():
    authorization_header = request.headers.get("Authorization")

    if (authorization_header is None) or (len(authorization_header.split(" ")) < 2):
        return None

    return authorization_header.split(" ")[1]


def get_jwt_token_payload():
    token = get_jwt_token()
    return jwt.decode(token, SECRET_JWT, algorithms="HS256", verify=False)


def get_token_payload():
    token = get_jwt_token()
    return jwt.decode(token, SECRET_JWT, algorithms="HS256", verify=True)


def is_authenticated(wrapped_function):
    def decorator(*args, **kwargs):
        token = get_jwt_token()

        if token is None:
            return {
                "error": "Invalid authorization header"
            }, 403

        try:
            token_payload = jwt.decode(token, SECRET_JWT, algorithms="HS256", verify=True)
        except Exception as e:
            print(e)
            return {
                "error": "Invalid authorization header"
            }, 403

        pk = token_payload["id"]

        stmt = select(User).where(User.id == pk)
        user = db.session.execute(stmt).first()

        if user is None:
            return {
                "error": "Invalid authorization header"
            }, 403

        return wrapped_function(*args, **kwargs)

    return decorator
