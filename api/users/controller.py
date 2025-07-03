from api.users import model as user_model


def is_valid_email(email):
    return "@" in email and "." in email


def register_user_logic(data):
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")

    if not all([first_name, last_name, email, password]):
        return {"error": "All fields are required."}, 400
    if not is_valid_email(email):
        return {"error": "Invalid email format."}, 400
    if len(password) < 4:
        return {"error": "Password must be at least 4 characters long."}, 400
    if user_model.check_email_exists(email):
        return {"error": "Email already registered."}, 409

    new_user = user_model.add_user(first_name, last_name, email, password)
    return new_user, 201


def login_user_logic(data):
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return {"error": "Email and password are required."}, 400

    user = user_model.get_user_by_credentials(email, password)
    if not user:
        return {"error": "Invalid email or password."}, 401

    return user, 200
