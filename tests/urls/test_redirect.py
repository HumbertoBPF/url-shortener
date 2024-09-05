import pytest

from database.config import db

base_url = "/redirect"


def test_redirect_requires_authentication(client):
    response = client.get(f"{base_url}/invalid")
    assert response.status_code == 403
    assert response.json["error"] == "Invalid authorization header"


def test_redirect_requires_authorization_headers(client):
    response = client.get(f"{base_url}/invalid", headers={"Authorization": "invalid"})
    assert response.status_code == 403
    assert response.json["error"] == "Invalid authorization header"


@pytest.mark.usefixtures("app_ctx")
def test_redirect_not_found(client, user):
    db.session.add(user)

    response = client.get(f"{base_url}/invalid", headers={"Authorization": f"Bearer {user.issue_token()}"})

    assert response.status_code == 404
    assert response.json["error"] == "Not found"

    db.session.close()


@pytest.mark.usefixtures("app_ctx")
def test_redirect(client, user, url):
    db.session.add(user)
    db.session.add(url)

    response = client.get(f"{base_url}/{url.short_url}", headers={"Authorization": f"Bearer {user.issue_token()}"})

    assert response.status_code == 302
    assert response.headers["Location"] == url.long_url

    db.session.close()
