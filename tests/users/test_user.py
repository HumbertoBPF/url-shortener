import pytest

from database.config import db

url = "/user"


def test_get_user_requires_token(client):
    response = client.get(url)
    assert response.status_code == 403


def test_get_user_requires_valid_token(client):
    response = client.get(url, headers={"Authorization": "Bearer invalid"})
    assert response.status_code == 403


@pytest.mark.usefixtures("app_ctx")
def test_get_user(client, user):
    db.session.add(user)

    response = client.get(url, headers={"Authorization": f"Bearer {user.issue_token()}"})

    assert response.status_code == 200
    assert response.json["email"] == user.email

    db.session.close()
