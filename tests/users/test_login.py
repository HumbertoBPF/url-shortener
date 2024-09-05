import pytest

from database.config import db

url = "/login"


@pytest.mark.usefixtures("app_ctx")
def test_login_invalid_email(client, user):
    db.session.add(user)

    response = client.post(url, json={
        "email": f"a{user.email}",
        "password": "str0ng-P@ssw0rd"
    })

    assert response.status_code == 403
    assert response.json["error"] == "Invalid credentials"


@pytest.mark.usefixtures("app_ctx")
def test_login_invalid_password(client, user):
    db.session.add(user)

    response = client.post(url, json={
        "email": user.email,
        "password": "Str0ng-P@ssw0rd"
    })

    assert response.status_code == 403
    assert response.json["error"] == "Invalid credentials"


@pytest.mark.usefixtures("app_ctx")
def test_login(client, user):
    db.session.add(user)

    response = client.post(url, json={
        "email": user.email,
        "password": "str0ng-P@ssw0rd"
    })

    assert response.status_code == 200
    assert "token" in response.json
