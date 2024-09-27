from flask import request
from marshmallow import ValidationError
from sqlalchemy import select

from database.config import db
from database.models import User
from schemas import LoginSchema, SignupSchema, UserSchema
from utils.authorization import get_token_payload, is_authenticated
from utils.cors import MethodViewWithCors, cors
from utils.hashing import hash_password


class LoginView(MethodViewWithCors):
    @cors
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


class SignupView(MethodViewWithCors):
    @cors
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


class UserView(MethodViewWithCors):
    @cors
    @is_authenticated
    def get(self):
        token_payload = get_token_payload()
        pk = token_payload["id"]

        stmt = select(User).where(User.id == pk)
        user = db.session.execute(stmt).first()

        schema = UserSchema()
        response_body = schema.dump(user[0])

        db.session.close()
        return response_body, 200
