import pytest
from sqlalchemy import select

from database.config import db
from database.models import User

url = "/signup"


def test_signup_requires_email(client):
    response = client.post(url, json={
        "password": "str0ng-P@ssw0rd"
    })

    assert response.status_code == 400
    assert response.json["email"] == ["Missing data for required field."]


def test_signup_requires_password(client, faker):
    response = client.post(url, json={
        "email": faker.email()
    })

    assert response.status_code == 400
    assert response.json["password"] == ["Missing data for required field."]


@pytest.mark.usefixtures("app_ctx")
def test_signup_requires_unique_email(client, user):
    db.session.add(user)

    response = client.post(url, json={
        "email": user.email,
        "password": "str0ng-P@ssw0rd"
    })

    assert response.status_code == 400
    assert response.json["email"] == ["This field must be unique."]

    db.session.close()


@pytest.mark.usefixtures("app_ctx")
def test_signup(client, faker):
    payload = {
        "email": faker.email(),
        "password": "str0ng-P@ssw0rd"
    }
    response = client.post(url, json=payload)

    assert response.status_code == 201

    stmt = select(User).where(User.email == payload["email"])
    new_user = db.session.execute(stmt).first()[0]

    assert new_user.check_password(payload["password"])

    db.session.close()
