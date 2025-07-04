# api/likes/routes.py
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


@likes_blueprint.route("/report", methods=["GET"])
def get_all_liked_vacations_report():
    response, status_code = like_controller.get_all_liked_vacations_report_logic()
    return jsonify(response), status_code


@likes_blueprint.route("/<int:user_id>", methods=["GET"])
def get_liked_vacations(user_id):
    response, status_code = like_controller.get_liked_vacations_logic(user_id)
    return jsonify(response), status_code