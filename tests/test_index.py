import pytest
from App.db import get_db



def test_index(app, client, auth):
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/")
    with open("test.txt", "w") as f:
        f.writelines(str(response.data))
    assert b"Log Out" in response.data

    with app.app_context():
        db = get_db()
        db.execute("""INSERT INTO post (offerer, email, title, body, subject, grade_from, grade_to, created)
        VALUES
        (1, 'test.test@gmail.com', 'test title2', 'test' || x'0a' || 'body', 'deutsch,englisch,mathe', 5, 7, '2022-01-01 00:00:00')""")
        db.execute("""INSERT INTO post (offerer, email, title, body, subject, grade_from, grade_to, created)
        VALUES
        (1, 'test.test@gmail.com', 'test title3', 'test' || x'0a' || 'body', 'deutsch,englisch,mathe', 5, 7, '2022-01-01 00:00:00')""")
        response = client.get("/")
        assert b"Anzeigen" in response.data
    