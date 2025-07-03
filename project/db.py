import sqlite3
from flask import g as myDB

DB_FILE = "database.db"


def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    if "db" not in myDB:
        myDB.db = sqlite3.connect(DB_FILE, timeout=15)
        myDB.db.row_factory = sqlite3.Row
        myDB.db.execute("PRAGMA foreign_keys = ON")
    return myDB.db


def close_db(e=None):
    """Closes the database again at the end of the request."""
    db = myDB.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    """Register database functions with the Flask app."""
    app.teardown_appcontext(close_db)
