import sqlite3
from project.db import get_db


def add_like(user_id, vacation_id):
    try:
        db = get_db()
        db.execute(
            "INSERT INTO likes (user_id, vacation_id) VALUES (?, ?)",
            (user_id, vacation_id),
        )
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def delete_like(user_id, vacation_id):
    db = get_db()
    result = db.execute(
        "DELETE FROM likes WHERE user_id = ? AND vacation_id = ?",
        (user_id, vacation_id),
    )
    db.commit()
    return result.rowcount > 0
