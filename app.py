from flask import Flask
from flask_cors import CORS

# --- NEW IMPORT ---
from project import db

# Import the blueprints
from api.users.routes import users_blueprint
from api.vacations.routes import vacations_blueprint
from api.likes.routes import likes_blueprint

# Create the Flask application instance
app = Flask(__name__)
CORS(app)

# --- NEW SETUP ---
# Initialize the database connection handling functions with the app
db.init_app(app)

# Register the blueprints, defining the URL prefix for each feature
app.register_blueprint(users_blueprint, url_prefix='/api/auth')
app.register_blueprint(vacations_blueprint, url_prefix='/api/vacations')
app.register_blueprint(likes_blueprint, url_prefix='/api/likes')

# The main entry point to run the app
if __name__ == '__main__':
    app.run(debug=True, port=5001)
    