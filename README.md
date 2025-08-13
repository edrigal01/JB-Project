# Vacation Management API

A Flask-based API for managing vacation packages. Users can register, log in, browse vacations, and "like" their favorite ones. Administrators have additional privileges to add, update, and delete vacation packages.

## Features

*   **User Authentication:** User registration and login.
*   **Role-based Access Control:** 'Admin' and 'User' roles with different permissions.
*   **Vacation Management:** Admins can create, read, update, and delete (CRUD) vacation packages.
*   **Vacation Likes:** Users can like and unlike vacations.
*   **Reporting:** Admins can view a report of which vacations are the most popular based on likes.

## Technologies Used

*   **Backend:** Python, Flask
*   **Database:** SQLite
*   **CORS Handling:** Flask-CORS

## Setup and Installation

1.  **Prerequisites:**
    *   Python 3.x
    *   `pip` for package management

2.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up the database:**
    This command creates a `database.db` file with the necessary tables and populates it with seed data.
    ```bash
    python scripts/database_setup.py
    ```

5.  **Run the application:**
    ```bash
    python app.py
    ```
    The API will be available at `http://127.0.0.1:5001`.

## API Endpoints

### Users

*   **Register a new user**
    *   `POST /api/auth/register`
    *   **Body:**
        ```json
        {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "password123"
        }
        ```

*   **Log in a user**
    *   `POST /api/auth/login`
    *   **Body:**
        ```json
        {
            "email": "test@example.com",
            "password": "password123"
        }
        ```

### Vacations

*   **Get all vacations**
    *   `GET /api/vacations/`

*   **Get a single vacation**
    *   `GET /api/vacations/<vacation_id>`

*   **Add a new vacation (Admin only)**
    *   `POST /api/vacations/`
    *   **Body:**
        ```json
        {
            "country_id": 1,
            "description": "A new amazing vacation",
            "start_date": "2026-01-01",
            "end_date": "2026-01-10",
            "price": 2500,
            "image_file_name": "new_vacation.jpg"
        }
        ```

*   **Update a vacation (Admin only)**
    *   `PUT /api/vacations/<vacation_id>`
    *   **Body:** (same as POST)

*   **Delete a vacation (Admin only)**
    *   `DELETE /api/vacations/<vacation_id>`

### Likes

*   **Like a vacation**
    *   `POST /api/likes/`
    *   **Body:**
        ```json
        {
            "user_id": 2,
            "vacation_id": 4
        }
        ```

*   **Unlike a vacation**
    *   `DELETE /api/likes/`
    *   **Body:**
        ```json
        {
            "user_id": 2,
            "vacation_id": 4
        }
        ```

*   **Get liked vacations for a user**
    *   `GET /api/likes/<user_id>`

*   **Get likes report (Admin only)**
    *   `GET /api/likes/report`

## Running Tests

The repository includes a couple of scripts for testing:

*   To generate a Postman collection for testing the API, run:
    ```bash
    python tests/generate_postman_collection.py
    ```
    This will create a `vacations_api_collection.json` file that you can import into Postman.

*   To run a series of automated API tests, execute the following script:
    ```bash
    python tests/run_verbose_api_tests.py
    ```
