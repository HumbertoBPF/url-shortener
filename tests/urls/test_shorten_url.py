import pytest
from sqlalchemy import select

from database.config import db
from database.models import Url

url = "/shorten"


def test_shorten_url_requires_authentication(client):
    response = client.post(url)
    assert response.status_code == 403
    assert response.json["error"] == "Invalid authorization header"


def test_shorten_url_invalid_authorization_headers(client):
    response = client.post(url, headers={"Authorization": "invalid"})
    assert response.status_code == 403
    assert response.json["error"] == "Invalid authorization header"


@pytest.mark.usefixtures("app_ctx")
def test_shorten_url_requires_url(client, user):
    db.session.add(user)

    response = client.post(url, json={}, headers={"Authorization": f"Bearer {user.issue_token()}"})

    assert response.status_code == 400
    assert response.json["long_url"] == ["Missing data for required field."]

    db.session.close()


@pytest.mark.usefixtures("app_ctx")
def test_shorten_url_requires_invalid_url(client, user):
    db.session.add(user)

    response = client.post(url, json={
        "long_url": "invalid"
    }, headers={"Authorization": f"Bearer {user.issue_token()}"})

    assert response.status_code == 400
    assert response.json["long_url"] == ["Not a valid URL."]

    db.session.close()


@pytest.mark.usefixtures("app_ctx")
def test_shorten_url_requires_invalid_url(client, user, faker):
    db.session.add(user)

    payload = {
        "long_url": faker.url()
    }

    response = client.post(url, json=payload, headers={"Authorization": f"Bearer {user.issue_token()}"})

    assert response.status_code == 201

    stmt = select(Url).where((Url.long_url == payload["long_url"]) and (Url.user_id == user.id))
    new_url = db.session.execute(stmt).first()[0]

    assert new_url.short_url == "1"

    db.session.close()
