from marshmallow import Schema, fields


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class SignupSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class ShortenUrlSchema(Schema):
    long_url = fields.Url(required=True)


class UrlSchema(Schema):
    id = fields.Int()
    short_url = fields.Str()
    long_url = fields.Str()


class UserSchema(Schema):
    email = fields.Email()
