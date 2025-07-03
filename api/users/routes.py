from flask import Blueprint, request, jsonify
from api.users import controller as user_controller

users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    response, status_code = user_controller.register_user_logic(data)
    return jsonify(response), status_code


@users_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    response, status_code = user_controller.login_user_logic(data)
    return jsonify(response), status_code
