# api/likes/model.py
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


def get_liked_vacations_by_user(user_id):
    db = get_db()
    liked_vacations = db.execute(
        """
        SELECT v.*
        FROM vacations v
        INNER JOIN likes l ON v.vacation_id = l.vacation_id
        WHERE l.user_id = ?
        ORDER BY v.start_date ASC
        """,
        (user_id,),
    ).fetchall()
    return [dict(row) for row in liked_vacations]


def get_all_liked_vacations_report():
    db = get_db()
    report = db.execute(
        """
        SELECT
            v.vacation_id,
            v.description,
            c.country_name,
            COUNT(l.user_id) as like_count
        FROM vacations v
        JOIN likes l ON v.vacation_id = l.vacation_id
        JOIN countries c ON v.country_id = c.country_id
        GROUP BY v.vacation_id
        ORDER BY like_count DESC
        """
    ).fetchall()
    return [dict(row) for row in report]