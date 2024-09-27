from flask import request, redirect
from marshmallow import ValidationError
from sqlalchemy import select

from database.config import db
from database.models import User, Url
from schemas import ShortenUrlSchema, UrlSchema
from utils.authorization import is_authenticated, get_jwt_token_payload
from utils.cors import MethodViewWithCors, cors
from utils.url import shorten_url


class UrlView(MethodViewWithCors):
    @cors
    @is_authenticated
    def post(self):
        try:
            request_body = ShortenUrlSchema().load(request.json)
        except ValidationError as e:
            return e.messages, 400

        token_payload = get_jwt_token_payload()
        user_id = token_payload["id"]

        user = db.session.get(User, user_id)

        url = Url(
            short_url="",
            long_url=request_body["long_url"],
            user_id=user.id
        )
        db.session.add(url)
        db.session.commit()

        url.short_url = shorten_url(url.id)
        db.session.add(url)
        db.session.commit()

        url_schema = UrlSchema()
        response_body = url_schema.dump(url)

        db.session.close()

        return response_body, 201


class RedirectView(MethodViewWithCors):
    @cors
    @is_authenticated
    def get(self, short_url):
        token_payload = get_jwt_token_payload()
        user_id = token_payload["id"]

        url_stmt = select(
            Url.long_url
        ).where(
            (Url.user_id == user_id) and (Url.short_url == short_url)
        )

        result = db.session.execute(url_stmt).first()

        if result is None:
            return {
                "error": "Not found"
            }, 404

        redirect_url = result[0]

        db.session.close()

        return redirect(redirect_url)
