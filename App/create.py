import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from App.db import get_db


bp = Blueprint("create", __name__)

subjects1 = {"deutsch", "englisch", "mathe", "physik", "geschichte",}
subjects2 = {"erdkunde", "religion", "politik", "biologie", "chemie"}

@bp.route("/create")
def create():
    if request.method == "POST":
        pass
    return render_template("main/create.html", subjects1=subjects1, subjects2=subjects2)