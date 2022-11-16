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
        username = request.form["usedrname"]
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


