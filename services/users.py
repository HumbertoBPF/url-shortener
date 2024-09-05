from flask import request
from flask.views import MethodView
from marshmallow import ValidationError
from sqlalchemy import select

from database.config import db
from database.models import User
from schemas import LoginSchema, SignupSchema
from utils.hashing import hash_password


class LoginView(MethodView):
    def post(self):
        schema = LoginSchema()

        try:
            request_body = schema.load(request.json)
        except ValidationError as e:
            return e.messages, 400

        email = request_body["email"]
        password = request_body["password"]

        stmt = select(User).where(User.email == email)
        user = db.session.execute(stmt).first()

        if user is None:
            return {
                "error": "Invalid credentials"
            }, 403

        user = user[0]

        if user.check_password(password):
            return {
                "token": user.issue_token()
            }, 200

        return {
            "error": "Invalid credentials"
        }, 403


class SignupView(MethodView):
    def post(self):
        schema = SignupSchema()

        try:
            request_body = schema.load(request.json)
        except ValidationError as e:
            return e.messages, 400

        email = request_body["email"]
        password = request_body["password"]

        stmt = select(User).where(User.email == email)
        user = db.session.execute(stmt).first()
        # TODO Avoid enumeration attacks later
        if user is not None:
            return {
                "email": ["This field must be unique."]
            }, 400

        user = User(
            email=email,
            password=hash_password(password)
        )
        db.session.add(user)
        db.session.commit()

        return "", 201
