# api\vacations\controller.py
from datetime import datetime
from api.vacations import model as vacation_model


def add_vacation_logic(data):
    required_fields = [
        "country_id",
        "description",
        "start_date",
        "end_date",
        "price",
        "image_file_name",
    ]
    if not all(field in data for field in required_fields):
        return {"error": "Missing one or more required fields."}, 400

    try:
        price = float(data["price"])
        start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return {"error": "Invalid price or date format. Use YYYY-MM-DD for dates."}, 400

    if not (0 < price <= 10000):
        return {"error": "Price must be between 0 and 10,000."}, 400
    if end_date < start_date:
        return {"error": "End date cannot be before start date."}, 400
    if start_date < datetime.now().date():
        return {"error": "Cannot add a vacation with a start date in the past."}, 400

    new_vacation = vacation_model.add_vacation(**data)
    return new_vacation, 201


def update_vacation_logic(vacation_id, data):
    if not vacation_model.get_vacation_by_id(vacation_id):
        return {"error": "Vacation not found."}, 404

    required_fields = ["country_id", "description", "start_date", "end_date", "price"]
    if not all(field in data for field in required_fields):
        return {"error": "Missing one or more required fields."}, 400

    try:
        price = float(data["price"])
        start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return {"error": "Invalid price or date format."}, 400

    if not (0 < price <= 10000):
        return {"error": "Price must be between 0 and 10,000."}, 400
    if end_date < start_date:
        return {"error": "End date cannot be before start date."}, 400

    image_file_name = data.get("image_file_name")
    updated_vacation = vacation_model.update_vacation(
        vacation_id,
        data["country_id"],
        data["description"],
        data["start_date"],
        data["end_date"],
        price,
        image_file_name,
    )
    return updated_vacation, 200


def delete_vacation_logic(vacation_id):
    if vacation_model.delete_vacation(vacation_id):
        return {"message": "Vacation deleted successfully."}, 204
    else:
        return {"error": "Vacation not found."}, 404
