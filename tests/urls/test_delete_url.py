import random

import pytest
from sqlalchemy import select

from database.config import db
from database.models import Url


@pytest.mark.usefixtures("app_ctx")
def test_delete_url_requires_authentication(client, url):
    db.session.add(url)
    response = client.delete(f"/urls/{url.id}")
    assert response.status_code == 403
    db.session.close()


@pytest.mark.usefixtures("app_ctx")
def test_delete_url_requires_valid_token(client, url):
    db.session.add(url)
    response = client.delete(f"/urls/{url.id}", headers={"Authorization": "Bearer invalid"})
    assert response.status_code == 403
    db.session.close()


@pytest.mark.usefixtures("app_ctx")
def test_delete_url_not_found(client, user, url):
    db.session.add(user)
    db.session.add(url)

    response = client.delete(
        f"/urls/{random.randint(10000, 20000)}",
        headers={"Authorization": f"Bearer {user.issue_token()}"}
    )

    assert response.status_code == 404
    assert response.json["error"] == "Not found"

    db.session.close()


@pytest.mark.usefixtures("app_ctx")
def test_delete_url(client, user, url):
    db.session.add(user)
    db.session.add(url)

    response = client.delete(f"/urls/{url.id}", headers={"Authorization": f"Bearer {user.issue_token()}"})

    assert response.status_code == 204

    stmt = select(Url).where(Url.id == url.id)
    assert db.session.execute(stmt).first() is None

    db.session.close()
