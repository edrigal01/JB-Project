import json
import uuid
from urllib.parse import urlparse


# --- Helper function for Postman URL structure ---
def parse_url_components(original_url):
    """
    Parses a URL into Postman's required URL structure.
    This version correctly identifies and defines Postman path variables (e.g., {{variable}}).
    """
    BASE_URL_TO_REPLACE = "http://127.0.0.1:5001"
    postman_raw_url = original_url.replace(BASE_URL_TO_REPLACE, "{{baseURL}}")

    try:
        parsed = urlparse(original_url)

        path_segments = [p for p in parsed.path.split("/") if p]

        # --- THIS IS THE CORRECTED LOGIC ---
        postman_path = []
        postman_variables = []
        for segment in path_segments:
            # Check if a segment is a Postman variable (e.g., {{vacation_id}})
            if segment.startswith("{{") and segment.endswith("}}"):
                # Extract the variable name without the braces
                var_name = segment[2:-2]
                # In the path, use the colon-prefixed placeholder syntax
                postman_path.append(f":{var_name}")
                # Add a definition to the URL's variable list
                postman_variables.append(
                    {
                        "key": var_name,
                        "value": segment,  # The value is the full {{...}} expression
                        "description": f"Variable for the '{var_name}' path segment.",
                    }
                )
            else:
                # It's a static path segment
                postman_path.append(segment)

        url_object = {
            "raw": postman_raw_url,
            "protocol": parsed.scheme,
            "host": parsed.hostname.split("."),
            "port": str(parsed.port),
            "path": postman_path,
        }

        # Only add the 'variable' key if we found path variables
        if postman_variables:
            url_object["variable"] = postman_variables

        return url_object

    except Exception as e:
        print(f"Error parsing URL '{original_url}': {e}")
        return {"raw": postman_raw_url, "host": [], "path": []}


def create_postman_request(
    name,
    method,
    url,
    headers=None,
    body=None,
    body_mode="raw",
    description="",
    test_script="",
):
    """Creates a dictionary representing a single Postman request item. (No changes here)"""
    item = {
        "name": name,
        "request": {
            "method": method,
            "header": [],
            "url": parse_url_components(url),
            "description": description,
        },
        "response": [],
    }
    if headers:
        for key, value in headers.items():
            item["request"]["header"].append({"key": key, "value": value})
    if body is not None:
        item["request"]["body"] = {
            "mode": body_mode,
            "raw": (
                json.dumps(body, indent=4)
                if isinstance(body, dict) and body_mode == "raw"
                else str(body)
            ),
        }
        if body_mode == "raw" and isinstance(body, dict):
            if not any(
                h["key"].lower() == "content-type" for h in item["request"]["header"]
            ):
                item["request"]["header"].append(
                    {"key": "Content-Type", "value": "application/json"}
                )
    if test_script:
        item["event"] = [
            {
                "listen": "test",
                "script": {"type": "text/javascript", "exec": test_script.splitlines()},
            }
        ]
    return item


def create_postman_folder(name, description, items):
    """Creates a dictionary representing a Postman folder. (No changes here)"""
    return {"name": name, "description": description, "item": items}


def generate_postman_collection(collection_name, items_list, description=""):
    """Generates the full Postman Collection JSON structure. (No changes here)"""
    collection = {
        "info": {
            "_postman_id": str(uuid.uuid4()),
            "name": collection_name,
            "description": description,
            "schema": "https://schema.postman.com/json/collection/v2.1.0/collection.json",
        },
        "item": items_list,
        "variable": [
            {
                "key": "baseURL",
                "value": "http://127.0.0.1:5001",
                "type": "string",
                "description": "The base URL for your API server.",
            },
            {
                "key": "vacation_id",
                "value": "1",
                "type": "string",
                "description": "An example ID for a vacation. Can be updated by tests.",
            },
            {
                "key": "user_id",
                "value": "1",
                "type": "string",
                "description": "An example ID for a user.",
            },
        ],
    }
    return collection


# --- Main Script to Define and Generate the Postman Collection ---
def create_project_proof_of_concept_collection():
    """Constructs the Postman collection based on the 9 finalized endpoints."""
    BASE_URL = "http://127.0.0.1:5001"
    collection_folders = []

    # --- 1. Authentication Endpoints ---
    auth_requests = [
        create_postman_request(
            name="1. Register a User",
            method="POST",
            url=f"{BASE_URL}/auth/register",
            body={
                "first_name": "Test",
                "last_name": "User",
                "email": "user@example.com",
                "password": "password123",
            },
            description="Create a new user account.",
        ),
        create_postman_request(
            name="2. Login User",
            method="POST",
            url=f"{BASE_URL}/auth/login",
            body={"email": "user@example.com", "password": "password123"},
            description="Authenticate a user and receive a token.",
        ),
    ]
    collection_folders.append(
        create_postman_folder(
            "Authentication",
            "Endpoints for user registration and login.",
            auth_requests,
        )
    )

    # --- 2. Vacation Management Endpoints ---
    vacation_requests = [
        create_postman_request(
            name="3. Get All Vacations",
            method="GET",
            url=f"{BASE_URL}/api/vacations",
            description="Retrieve a list of all vacation entries.",
        ),
        create_postman_request(
            name="4. Get Vacation by ID",
            method="GET",
            url=f"{BASE_URL}/api/vacations/{{vacation_id}}",
            description="Retrieve details for a single vacation using its ID.",
        ),
        create_postman_request(
            name="5. Add New Vacation",
            method="POST",
            url=f"{BASE_URL}/api/vacations",
            body={
                "country_id": 1,
                "description": "A beautiful trip to the mountains.",
                "start_date": "2024-10-01",
                "end_date": "2024-10-10",
                "price": 1999.99,
                "image_file_name": "mountains.jpg",
            },
            description="Create a new vacation entry. (Requires Admin privileges)",
            test_script="""
                if (pm.response.code === 201) {
                    var jsonData = pm.response.json();
                    if (jsonData && jsonData.vacation_id) {
                        pm.collectionVariables.set("vacation_id", jsonData.vacation_id);
                    }
                }
            """,
        ),
        create_postman_request(
            name="6. Update Existing Vacation",
            method="PUT",
            url=f"{BASE_URL}/api/vacations/{{vacation_id}}",
            body={
                "country_id": 1,
                "description": "UPDATED: An even more beautiful trip to the mountains.",
                "start_date": "2024-10-01",
                "end_date": "2024-10-12",
                "price": 2150.00,
                "image_file_name": "mountains_updated.jpg",
            },
            description="Modify an existing vacation entry. (Requires Admin privileges)",
        ),
        create_postman_request(
            name="7. Delete Vacation",
            method="DELETE",
            url=f"{BASE_URL}/api/vacations/{{vacation_id}}",
            description="Remove a vacation entry. (Requires Admin privileges)",
        ),
    ]
    collection_folders.append(
        create_postman_folder(
            "Vacation Management",
            "Endpoints for CRUD operations on vacations. (Admin-only for CUD)",
            vacation_requests,
        )
    )

    # --- 3. Like Functionality Endpoints ---
    like_requests = [
        create_postman_request(
            name="8. Like a Vacation",
            method="POST",
            url=f"{BASE_URL}/api/likes",
            body={
                "user_id": "{{user_id}}",  # Added user_id
                "vacation_id": "{{vacation_id}}",
            },
            description="Record a user's 'like' for a specific vacation. Both user_id and vacation_id are required in the body.",
        ),
        create_postman_request(
            name="9. Unlike a Vacation",
            method="DELETE",
            url=f"{BASE_URL}/api/likes",  # CORRECTED: URL should not contain the vacation_id
            body={  # CORRECTED: Body with user_id and vacation_id is required
                "user_id": "{{user_id}}",
                "vacation_id": "{{vacation_id}}",
            },
            description="Remove a user's 'like' from a specific vacation. The user_id and vacation_id must be in the JSON body.",
        ),
    ]
    collection_folders.append(
        create_postman_folder(
            "Like Functionality",
            "Endpoints for users to like and unlike vacations.",
            like_requests,
        )
    )

    return generate_postman_collection(
        collection_name="Vacations Project - API Proof of Concept",
        items_list=collection_folders,
        description="The 9 definitive API endpoints for the Vacations project, generated for proof-of-concept demonstration.",
    )


if __name__ == "__main__":
    postman_collection = create_project_proof_of_concept_collection()
    output_filename = "vacations_project_poc_collection.json"
    with open(output_filename, "w") as f:
        json.dump(postman_collection, f, indent=4)
    print(f"✅ Postman collection '{output_filename}' generated successfully!")
    print("\n--- Next Steps ---")
    print("This version restores the 'smarter' path variable handling.")
    print(
        "When you import and view a request like 'Get Vacation by ID', you will now see the 'Path Variables' editor in the Postman UI."
    )
