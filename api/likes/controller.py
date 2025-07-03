from api.likes import model as like_model


def add_like_logic(data):
    user_id = data.get("user_id")
    vacation_id = data.get("vacation_id")
    if not all([user_id, vacation_id]):
        return {"error": "user_id and vacation_id are required."}, 400

    if like_model.add_like(user_id, vacation_id):
        return {"message": "Like added successfully."}, 201
    else:
        return {
            "error": "Failed to add like. It may already exist or user/vacation is invalid."
        }, 409


def delete_like_logic(data):
    user_id = data.get("user_id")
    vacation_id = data.get("vacation_id")
    if not all([user_id, vacation_id]):
        return {"error": "user_id and vacation_id are required."}, 400

    if like_model.delete_like(user_id, vacation_id):
        return {"message": "Like removed successfully."}, 204
    else:
        return {"error": "Like not found."}, 404
