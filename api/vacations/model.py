# api\vacations\model.py
from project.db import get_db


def get_all_vacations_sorted():
    db = get_db()
    vacations = db.execute("SELECT * FROM vacations ORDER BY start_date ASC").fetchall()
    return [dict(row) for row in vacations]


def add_vacation(country_id, description, start_date, end_date, price, image_file_name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO vacations (country_id, description, start_date, end_date, price, image_file_name) VALUES (?, ?, ?, ?, ?, ?)",
        (country_id, description, start_date, end_date, price, image_file_name),
    )
    vacation_id = cursor.lastrowid
    db.commit()
    new_vacation = db.execute(
        "SELECT * FROM vacations WHERE vacation_id = ?", (vacation_id,)
    ).fetchone()
    return dict(new_vacation)


def update_vacation(
    vacation_id, country_id, description, start_date, end_date, price, image_file_name
):
    db = get_db()
    if image_file_name:
        db.execute(
            "UPDATE vacations SET country_id = ?, description = ?, start_date = ?, end_date = ?, price = ?, image_file_name = ? WHERE vacation_id = ?",
            (
                country_id,
                description,
                start_date,
                end_date,
                price,
                image_file_name,
                vacation_id,
            ),
        )
    else:
        db.execute(
            "UPDATE vacations SET country_id = ?, description = ?, start_date = ?, end_date = ?, price = ? WHERE vacation_id = ?",
            (country_id, description, start_date, end_date, price, vacation_id),
        )
    db.commit()
    updated_vacation = db.execute(
        "SELECT * FROM vacations WHERE vacation_id = ?", (vacation_id,)
    ).fetchone()
    return dict(updated_vacation)


def delete_vacation(vacation_id):
    db = get_db()
    result = db.execute("DELETE FROM vacations WHERE vacation_id = ?", (vacation_id,))
    db.commit()
    return result.rowcount > 0


def get_vacation_by_id(vacation_id):
    db = get_db()
    vacation = db.execute(
        "SELECT * FROM vacations WHERE vacation_id = ?", (vacation_id,)
    ).fetchone()
    return dict(vacation) if vacation else None
