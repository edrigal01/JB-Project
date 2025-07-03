from flask import Blueprint, request, jsonify
from api.likes import controller as like_controller

likes_blueprint = Blueprint("likes", __name__)


@likes_blueprint.route("/", methods=["POST"])
def add_like():
    data = request.get_json()
    response, status_code = like_controller.add_like_logic(data)
    return jsonify(response), status_code


@likes_blueprint.route("/", methods=["DELETE"])
def delete_like():
    data = request.get_json()
    response, status_code = like_controller.delete_like_logic(data)
    return jsonify(response), status_code
