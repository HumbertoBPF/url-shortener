import pytest

from app_factory import create_app
from database.config import db
from database.models import User, Url
from utils.hashing import hash_password
from utils.url import shorten_url


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def app_ctx(app):
    with app.app_context():
        yield


@pytest.fixture
def user(app, faker):
    with app.app_context():
        user = User(
            email=faker.email(),
            password=hash_password("str0ng-P@ssw0rd")
        )
        db.session.add(user)
        db.session.commit()
        db.session.close()
    return user


@pytest.fixture
def url(app, user, faker):
    with app.app_context():
        db.session.add(user)

        url = Url(
            short_url="",
            long_url=faker.url(),
            user_id=user.id
        )
        db.session.add(url)
        db.session.commit()

        url.short_url = shorten_url(url.id)
        db.session.commit()

        db.session.close()
    return url
