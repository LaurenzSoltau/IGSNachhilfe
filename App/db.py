import sqlite3

import click
from flask import current_app, g


# connect to the database and load it into the g object. For further request, check g object still has a db if not load it again
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # tells the connection to return rows that behave like dictionaries allowing to acces the colums by name
        g.db.row_factory = sqlite3.Row
    
    return g.db

# checks if a connection was created. If yes it gets closed
def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

# Run the sql in schema
def init_db():
    db = get_db()
    
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# defines a command line command called init-db that calls the init function and creates the database
@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


# takes the app as an argument and register close_db and the init_db_command
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)