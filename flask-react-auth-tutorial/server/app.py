import os
import datetime
import jwt
from functools import wraps
from dotenv import load_dotenv
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

# Load environment variables from .env file
load_dotenv()

# -----------------
# App Initialization
# -----------------
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# Configure CORS to allow requests from the React client
client_origin = os.environ.get("CLIENT_ORIGIN")
if client_origin:
    CORS(app, resources={r"/*": {"origins": client_origin}})
else:
    # Fallback if CLIENT_ORIGIN is not set
    CORS(app)

# A simple in-memory dictionary to store users for demonstration purposes.
# In a real application, you would use a database.
users = {}
user_id_counter = 1

# -----------------
# Authentication Decorator
# -----------------
def require_auth(f):
    """
    A decorator to protect routes that require authentication.

    It extracts the JWT from the 'Authorization: Bearer <token>' header,
    validates it, and makes the user's identity available via Flask's `g` object.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        token = None

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Authentication token is missing!"}), 401

        try:
            # Decode the token using the secret key
            payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            # Store the user's identity in the g object for this request
            g.current_user = users.get(payload['user_id'])
            if g.current_user is None:
                return jsonify({"error": "User not found!"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401

        return f(*args, **kwargs)
    return decorated_function

# -----------------
# API Routes
# -----------------

@app.route("/")
def index():
    return jsonify({"message": "Flask server is running!"})

# --- Auth Routes ---
@app.route("/auth/register", methods=["POST"])
def register():
    """
    User registration endpoint.
    Hashes the password before storing the user.
    """
    global user_id_counter
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Check if user already exists
    if any(u['email'] == email for u in users.values()):
        return jsonify({"error": "User with this email already exists"}), 409

    # Hash the password for security
    hashed_password = generate_password_hash(password)

    new_user = {
        "id": user_id_counter,
        "email": email,
        "password": hashed_password
    }
    users[user_id_counter] = new_user
    user_id_counter += 1

    return jsonify({"message": "User registered successfully"}), 201

@app.route("/auth/login", methods=["POST"])
def login():
    """
    User login endpoint.
    Verifies credentials and returns a JWT upon success.
    """
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Find the user by email
    user_to_login = None
    for user in users.values():
        if user['email'] == email:
            user_to_login = user
            break

    if user_to_login and check_password_hash(user_to_login["password"], password):
        # Generate JWT
        token = jwt.encode({
            'user_id': user_to_login['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({"message": "Login successful", "token": token})

    return jsonify({"error": "Invalid credentials"}), 401

# --- Protected Route ---
@app.route("/api/protected", methods=["GET"])
@require_auth
def protected_route():
    """
    An example of a protected route.
    Only accessible to authenticated users.
    """
    # The user's identity is available via g.current_user thanks to the decorator
    logged_in_user = g.current_user
    return jsonify({
        "message": f"Hello, {logged_in_user['email']}! This is a protected resource.",
        "user_data": {
            "id": logged_in_user['id'],
            "email": logged_in_user['email']
        }
    })

# -----------------
# Main Execution
# -----------------
if __name__ == "__main__":
    # In a production environment, use a proper WSGI server like Gunicorn or uWSGI
    app.run(debug=True, port=5001)
