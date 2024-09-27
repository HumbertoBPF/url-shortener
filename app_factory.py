from flask import Flask

from database.config import db
from services.urls import UrlView, RedirectView
from services.users import LoginView, SignupView
from settings import ENVIRONMENT, DATABASE_URL


def create_app():
    app = Flask(__name__)

    uri = "sqlite+pysqlite:///:memory:" if ENVIRONMENT == "test" else DATABASE_URL
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.add_url_rule("/login", view_func=LoginView.as_view("login"))
    app.add_url_rule("/signup", view_func=SignupView.as_view("signup"))
    app.add_url_rule("/shorten", view_func=UrlView.as_view("url-shorten"))
    app.add_url_rule("/redirect/<string:short_url>", view_func=RedirectView.as_view("redirect"))

    return app
