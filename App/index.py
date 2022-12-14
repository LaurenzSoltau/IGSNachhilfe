import functools
import random

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from App.db import get_db


bp = Blueprint("index", __name__)

@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        "SELECT * FROM post"
    ).fetchall()
    length = len(posts)
    if length > 1:
        preview = random.sample(posts, k=length)
    else:
        preview = []


    return render_template("main/index.html", posts=preview)