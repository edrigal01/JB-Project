from project.db import get_db


def add_user(first_name, last_name, email, password):
    db = get_db()
    # By default, new users get role_id 2 (User)
    db.execute(
        "INSERT INTO users (first_name, last_name, email, password, role_id) VALUES (?, ?, ?, ?, 2)",
        (first_name, last_name, email, password),
    )
    db.commit()
    user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    return dict(user) if user else None


def get_user_by_credentials(email, password):
    db = get_db()
    # Return user details but omit the password for security
    user = db.execute(
        "SELECT user_id, first_name, last_name, email, role_id FROM users WHERE email = ? AND password = ?",
        (email, password),
    ).fetchone()
    return dict(user) if user else None


def check_email_exists(email):
    db = get_db()
    user = db.execute("SELECT user_id FROM users WHERE email = ?", (email,)).fetchone()
    return user is not None
