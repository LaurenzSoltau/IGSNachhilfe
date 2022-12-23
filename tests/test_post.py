import pytest
from App.db import get_db

def test_create(auth, client, app):
    auth.login()
    assert client.get("/create").status_code == 200
    client.post("/create", data={
        "title": "created",
        "body": "fwe",
        "email": "t.t@gmail.com",
        "grade_from": "2",
        "grade_to": "4",
        "mathe": "0",
        "englisch": "0",
        "geschichte": "0",
        "deutsch": 1, 
        "religion": "0",
        "politik": "0",
        "erdkunde": "0",
        "chemie": "0",
        "physik": "0",
        "biologie": "0",        
        })

    with app.app_context():
        db = get_db()
        count = db.execute(
            "SELECT COUNT(id) FROM post"
        ).fetchone()[0]
        assert count == 2
    

def test_update(client, auth, app):
    auth.login()
    assert client.get("/1/edit").status_code == 200
    client.post("/1/edit", data={
        "title": "updated", 
        "body": "f",
        "grade_from": "3",
        "grade_to": "6",
        })

    with app.app_context():
        db = get_db()
        post = db.execute(
            "SELECT * FROM post WHERE id = 1"
        ).fetchone()
        with open("test.txt", "w") as f:
            f.write(str(post["title"]))
        assert post["title"] == "updated"


@pytest.mark.parametrize("path", (
    "/create", 
    "/1/edit",
    ))
def test_create_edit_validate(client, auth, path):
    auth.login()
    if path == "/create":
        response = client.post("/create", data={
        "title": "",
        "body": "fwe",
        "email": "t.t@gmail.com",
        "grade_from": "2",
        "grade_to": "4",
        "mathe": "0",
        "englisch": "0",
        "geschichte": "0",
        "deutsch": 1, 
        "religion": "0",
        "politik": "0",
        "erdkunde": "0",
        "chemie": "0",
        "physik": "0",
        "biologie": "0",        
        })
        assert b"Inhalt deiner Anzeige" in response.data
    if path == "/1/edit":
        response = client.post("/1/edit", data={
        "title": "", 
        "body": "f",
        "grade_from": "3",
        "grade_to": "6",
        })
        assert b"Inhalt deiner Anzeige" in response.data

def test_delete(client, auth, app):
    auth.login()
    response = client.post("/1/delete")
    assert response.headers["Location"] == "/marketplace"

    with app.app_context():
        db = get_db()
        post = db.execute("SELECT * FROM post WHERE id = 1").fetchone()
        assert post is None