import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from App.db import get_db

# create blueprint named auth and the urls prefix auth
bp = Blueprint("auth", __name__, url_prefix="/auth")

# view to register a new user
@bp.route("/register", methods=["GET", "POST"])
def register():
    # if method is Post check inputs and load into database
    if request.method == "POST":
        # get the data from the form
        username = request.form["username"]
        password = request.form["password"]
        db = get_db() # load database
        error = None

        # guard clauses to validate inputs
        if not username:
            error = "Username required."
        elif not password:
            error = "Password required."

        # if the input is valid call database and save the new user in users
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)", 
                    (username, generate_password_hash(password)),
                )
            except db.IntegrityError:
                error = f"User {username} is already registered."
        
            else:
                return redirect(url_for("auth.login"))
        
        flash(error)


    return render_template("auth/register.html")


@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # get the data from the html form
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        # get the data from the database where username is equal to inputed username
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        # guardclauses to make sure the username and password is right if it exists
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        
        if error == None:
            session.clear()
            session["user_id"] = [user["id"]]
            return redirect(url_for("index"))

        flash(error)

        return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        
        return view(**kwargs)

    return wrapped_view
