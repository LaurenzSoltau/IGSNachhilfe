import pytest
from App.db import get_db


def test_marketplace(client, auth):
    response = client.get("/marketplace")
    assert b"test title" in response.data
    assert b"body" in response.data
    assert b"Kontakt" in response.data
    assert b"create" not in response.data
    assert b"change" not in response.data
    assert b"deutsch" in response.data

    auth.login()
    response = client.get("/marketplace")
    assert b"create" in response.data
    assert b"Bearbeiten" in response.data
    assert b"Delete" in response.data

@pytest.mark.parametrize('path', (
    '/create',
    '/1/edit',
    '/1/delete',
))
def test_login_required(client, path, auth): 
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_author_required(app, client, auth):
    with app.app_context():
        db = get_db()
        db.execute("UPDATE post SET offerer = 2 WHERE id = 1")
        db.commit()
    
    auth.login()

    assert client.post("/1/edit").status_code == 403
    assert client.post("/1/delete").status_code == 403

    assert b"href='/1/edit'" not in client.get("/").data


@pytest.mark.parametrize('path', (
    '/2/edit',
    '/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404