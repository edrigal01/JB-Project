# run_verbose_api_tests.py
# A script that runs and VISUALLY DEMONSTRATES API tests for the Vacations project.

import requests
import json
import time
from datetime import datetime, timedelta

# --- Configuration ---
BASE_URL = "http://127.0.0.1:5001/api"
DEFAULT_TIMEOUT = 10  # Seconds to wait for a response

# --- Central Request Function for Visibility ---
def make_request(method, url, json_payload=None):
    """
    Prints the details of the request, makes the request, and returns the response.
    This is the core function for showing what's happening.
    """
    # Announce the action
    endpoint = url.replace(BASE_URL, '') # Show a clean endpoint path
    print(f"\n▶️  Action: {method.upper()} request to endpoint '{endpoint}'")

    # If there's data, print it so the teacher can see what's being sent
    if json_payload:
        print("   Payload Sent:")
        # Use json.dumps for pretty printing the dictionary
        print(json.dumps(json_payload, indent=4))

    try:
        # Make the actual HTTP request
        response = requests.request(
            method,
            url,
            json=json_payload,
            timeout=DEFAULT_TIMEOUT
        )
        return response
    except requests.exceptions.RequestException as e:
        # Handle cases where the server is not running or there's a network error
        print(f"‼️  CRITICAL NETWORK ERROR: Could not connect to the server.")
        print(f"    Details: {e}")
        # Return a mock response object to prevent the script from crashing
        class MockResponse:
            status_code = 503
            text = f"Network Error: {e}"
            def json(self): return {"error": "Network request failed", "details": str(e)}
        return MockResponse()


# --- Helper Function for Printing Test Results ---
def print_test_result(validation_name, success, response=None, expected_status=None):
    """
    Prints a formatted result for a single validation check.
    """
    status_icon = "✅ PASS" if success else "❌ FAIL"
    print(f"\n   └── {status_icon} - Validation: {validation_name}")
    if not success and response is not None:
        print(f"       - Expected Status: {expected_status}, Got: {response.status_code}")
        try:
            print(f"       - Response Body:   {response.json()}")
        except json.JSONDecodeError:
            print(f"       - Response Text:   {response.text}")
    print("-" * 60)
    return success

# --- Main Test Execution Function ---
def run_api_scenarios():
    """
    Executes a series of API test scenarios in a logical, narrative order.
    """
    print("\n🚀🚀🚀 Starting API Demonstration Script 🚀🚀🚀")
    
    # Store IDs created during the test run to use in later steps
    created_ids = {}

    # =================================================================
    # --- SCENARIO 1: A REGULAR USER'S JOURNEY ---
    # =================================================================
    print("\n\n--- SCENARIO 1: A REGULAR USER'S JOURNEY ---")

    # 1.1: Register a brand new user
    new_user_email = f"testuser_{int(time.time())}@example.com"
    reg_payload = {
        "first_name": "Test", "last_name": "User",
        "email": new_user_email, "password": "strongpassword123"
    }
    response = make_request("post", f"{BASE_URL}/auth/register", json_payload=reg_payload)
    if print_test_result("New user is created successfully", response.status_code == 201, response, 201):
        created_ids['new_user_id'] = response.json().get('user_id')

    # 1.2: Log in as the newly created user
    login_payload = {"email": new_user_email, "password": "strongpassword123"}
    response = make_request("post", f"{BASE_URL}/auth/login", json_payload=login_payload)
    print_test_result(f"User can log in with correct credentials", response.status_code == 200, response, 200)

    # 1.3: View all vacations
    response = make_request("get", f"{BASE_URL}/vacations/")
    is_list = isinstance(response.json(), list) if response.ok else False
    print_test_result("User can retrieve a list of all vacations", response.status_code == 200 and is_list, response, 200)

    # =================================================================
    # --- SCENARIO 2: ADMIN CONTENT MANAGEMENT ---
    # =================================================================
    print("\n\n--- SCENARIO 2: ADMIN CONTENT MANAGEMENT ---")

    # 2.1: Log in as Admin
    admin_login_payload = {"email": "admin@vacations.com", "password": "admin123"}
    response = make_request("post", f"{BASE_URL}/auth/login", json_payload=admin_login_payload)
    print_test_result("Admin can log in successfully", response.status_code == 200, response, 200)

    # 2.2: Add a new vacation
    start_date = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=100)).strftime('%Y-%m-%d')
    vacation_payload = {
        "country_id": 5, "description": "A new automated test vacation to Phuket",
        "start_date": start_date, "end_date": end_date,
        "price": 3550.50, "image_file_name": "phuket_test.jpg"
    }
    response = make_request("post", f"{BASE_URL}/vacations/", json_payload=vacation_payload)
    if print_test_result("Admin can add a new vacation", response.status_code == 201, response, 201):
        created_ids['new_vacation_id'] = response.json().get('vacation_id')
    
    # This block only runs if the vacation was created successfully
    if 'new_vacation_id' in created_ids:
        vac_id = created_ids['new_vacation_id']
        
        # 2.3: Update the vacation that was just created
        update_payload = vacation_payload.copy()
        update_payload['price'] = 3700.00
        update_payload['description'] = "UPDATED: A fantastic test vacation to Phuket"
        
        response = make_request("put", f"{BASE_URL}/vacations/{vac_id}", json_payload=update_payload)
        price_is_updated = response.json().get('price') == 3700.00 if response.ok else False
        print_test_result(f"Admin can update the vacation (ID: {vac_id})", response.status_code == 200 and price_is_updated, response, 200)
        
        # 2.4: Delete the vacation
        response = make_request("delete", f"{BASE_URL}/vacations/{vac_id}")
        print_test_result(f"Admin can delete the vacation (ID: {vac_id})", response.status_code == 204, response, 204)

        # 2.5: Verify the vacation is truly gone by trying to get it again
        response = make_request("get", f"{BASE_URL}/vacations/{vac_id}")
        print_test_result(f"Verify vacation (ID: {vac_id}) is deleted", response.status_code == 404, response, 404)
    else:
        print("\n S K I P P I N G  - Update/Delete tests skipped because new vacation creation failed.")

    print("\n\n🏁🏁🏁 All scenarios completed. 🏁🏁🏁")

# --- Main Execution Block ---
if __name__ == "__main__":
    # A small delay to ensure the Flask server is ready to accept connections
    print("Waiting 1.5 seconds for server to be ready...")
    time.sleep(1.5)
    
    # Run all the test scenarios
    run_api_scenarios()