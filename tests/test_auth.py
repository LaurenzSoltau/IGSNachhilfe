import pytest
from flask import g, session
from App.db import get_db


def test_register(client, app):
    assert client.get("/auth/register").status_code == 200
    response = client.post(
        "/auth/register", data={"username": "a", "password": "a", "email": "a.a@gmail.com"}
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a' ",
        ).fetchone() is not None


@pytest.mark.parametrize(("username", "email", "password", "message"), (
    ("", "", "", b"Gib einen Username ein!"),
    ("a", "", "", b"Gib eine Email ein!"),
    ("a", "a", "", b"Gib ein Passwort ein!"),
    ("test", "test.test@gmail.com", "test", b"already registered")
))
def test_register_validate_input(client, username, email, password, message):
    response = client.post(
        "/auth/register",
        data={"username": username, "email": email, "password": password}
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    #response = auth.login()
    response = client.post(
        "/auth/login", data={"email": "test.test@gmail.com", "password": "test"}
    )
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'][0] == 1
        assert g.user['email'] == 'test.test@gmail.com'


@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('a', 'a', b'Incorrect Email.'),
    ('test.test@gmail.com', 'a', b'Incorrect password.'),
))
def test_login_validate_input(client, email, password, message):
    response = client.post(
        "/auth/login", data={"email": email, "password": password}
    )
    with open("test.txt", "w") as f:
        f.writelines(str(response.data))
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session