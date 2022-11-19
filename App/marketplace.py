import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from App.db import get_db


bp = Blueprint("marketplace", __name__)

@bp.route("/marketplace")
def marketplace():
    db = get_db()
    posts = db.execute(
        "SELECT * FROM post"
    ).fetchall()

    return render_template("main/marketplace.html", posts=posts)