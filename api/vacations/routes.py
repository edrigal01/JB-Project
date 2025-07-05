# api\vacations\routes.py
from flask import Blueprint, request, jsonify
from api.vacations import controller as vacation_controller
from api.vacations import model as vacation_model

vacations_blueprint = Blueprint("vacations", __name__)


@vacations_blueprint.route("/", methods=["GET"])
def get_all_vacations():
    vacations = vacation_model.get_all_vacations_sorted()
    return jsonify(vacations), 200


@vacations_blueprint.route("/", methods=["POST"])
def add_vacation():
    data = request.get_json()
    response, status_code = vacation_controller.add_vacation_logic(data)
    return jsonify(response), status_code


@vacations_blueprint.route("/<int:vacation_id>", methods=["PUT"])
def update_vacation(vacation_id):
    data = request.get_json()
    response, status_code = vacation_controller.update_vacation_logic(vacation_id, data)
    return jsonify(response), status_code


@vacations_blueprint.route("/<int:vacation_id>", methods=["DELETE"])
def delete_vacation(vacation_id):
    response, status_code = vacation_controller.delete_vacation_logic(vacation_id)
    return jsonify(response), status_code

@vacations_blueprint.route("/<int:vacation_id>", methods=["GET"])
def get_vacation_by_id(vacation_id):
    vacation = vacation_model.get_vacation_by_id(vacation_id)
    if vacation:
        return jsonify(vacation), 200
    else:
        return jsonify({"error": "Vacation not found."}), 404