import functools
from App.auth import login_required

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from App.db import get_db


bp = Blueprint("create", __name__)

subjects1 = {"deutsch", "englisch", "mathe", "physik", "geschichte",}
subjects2 = {"erdkunde", "religion", "politik", "biologie", "chemie"}



@bp.route("/create", methods=["POST", "GET"])
@login_required
def create():
    # if request is submitted by the form the the request and save post in database
    if request.method == "POST":
        email = request.form["email"]
        title = request.form["title"]
        body = request.form["body"]
        grade_from = request.form["grade_from"]
        grade_to = request.form["grade_to"]
        error = None
        # Fächer 
        subjects = {}
        subjects_list = [] # List containing all the picked subjects after the loops
        for subject in subjects1:
            subjects[subject] = request.form[subject]
        for subject in subjects2:
            subjects[subject] = request.form[subject]
        for subject in subjects:
            if subjects[subject] == "1":
                subjects_list.append(subject)
        subjects_string = ",".join(subjects_list)

        # guard clauses
        if not email:
            error = "E-mail Adresse notwendig."
        elif not title:
            error = "Bitte gib einen Titel ein."
        elif not body:
            error = "Bitte gibt den Inhalt an"
        elif not grade_from:
            error = "Bitte gib an ab welcher Klasse du Nachhilfe geben möchtest."
        elif not grade_to:
            error = "Bitte gib an bis zu welcher Klasse du Nachhilfe geben möchtest."
        elif grade_from > grade_to:
            error = "Deine Eingabe ergibt kein Sinn, prüfe nochmal welchen Klassen du nachhilfe geben möchtest."
        
        if error is None:
            # save post in Database
            try:
                db = get_db()
                db.execute(
                    "INSERT INTO post (offerer, email, title, body, subject, grade_from, grade_to) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (1, email, title, body, subjects_string, grade_from, grade_to,)
                )
                db.commit()
            except db.IntegrityError:
                error = "Es gibt bereits eine Anzeige mit diesem Titel."
            # return index page
            else:
                return redirect(url_for("index.index"))


        flash(error)
    # if user gets via get request show the create template
    return render_template("main/create.html", subjects1=subjects1, subjects2=subjects2)