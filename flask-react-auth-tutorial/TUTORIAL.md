# Tutorial: Building a Full-Stack App with Flask, React, and JWT Authentication

This tutorial guides you through building a complete full-stack web application featuring a Python Flask backend and a React frontend. The core focus is on implementing a secure authentication and authorization flow using JSON Web Tokens (JWTs).

## Table of Contents
1.  [Prerequisites](#prerequisites)
2.  [Project Structure](#project-structure)
3.  [Backend Setup (Flask)](#backend-setup-flask)
4.  [Frontend Setup (React)](#frontend-setup-react)
5.  [Running the Application](#running-the-application)
6.  [Security Best Practices](#security-best-practices)

---

## Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.x** and `pip`
- **Node.js** and `npm` (or `yarn`)

---

## Project Structure

We'll organize our application into two main directories inside the `flask-react-auth-tutorial` folder:

- `/server`: Contains our Python Flask backend.
- `/client`: Contains our React frontend application.

This separation keeps the backend and frontend concerns neatly organized.

```
/flask-react-auth-tutorial
├── client/
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.jsx
│       ├── api.js
│       └── index.js
├── server/
│   ├── .env
│   ├── app.py
│   └── requirements.txt
└── TUTORIAL.md
```

---

## Backend Setup (Flask)

Let's start by setting up the server.

### 1. Set Up a Virtual Environment

From the `server` directory, create and activate a Python virtual environment. This isolates our project's dependencies.

```bash
# Navigate to the server directory
cd server

# Create the virtual environment
python -m venv venv

# Activate it
# On Windows:
# venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate
```

### 2. Install Dependencies

We've listed all required Python packages in `requirements.txt`. Install them using `pip`.

**`server/requirements.txt`:**
```
Flask>=2.0
Flask-CORS>=3.0
PyJWT>=2.0
python-dotenv>=0.19
werkzeug>=2.0
```

**Installation Command:**
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

The `server/.env` file stores configuration variables. This practice keeps sensitive data like secret keys out of your source code.

**`server/.env`:**
```
SECRET_KEY=your_super_secret_key_change_me
CLIENT_ORIGIN=http://localhost:3000
```
- `SECRET_KEY`: A long, random string used to sign our JWTs. **You must change this for a production app.**
- `CLIENT_ORIGIN`: The URL of our React app. This is used by Flask-CORS to prevent requests from other origins.

### 4. The Flask Application (`app.py`)

This is the core of our backend. Let's break it down.

#### Initialization and CORS

```python
import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# Configure CORS
client_origin = os.environ.get("CLIENT_ORIGIN")
CORS(app, resources={r"/*": {"origins": client_origin}})
```
We load the environment variables, initialize Flask, and set up Cross-Origin Resource Sharing (CORS). CORS is essential to allow our React app (running on `localhost:3000`) to make requests to our Flask server (running on `localhost:5001`).

#### User Registration & Password Hashing

For simplicity, we use an in-memory dictionary as our user database. **In a real app, use a proper database (e.g., PostgreSQL, MySQL).**

```python
from werkzeug.security import generate_password_hash, check_password_hash

# ... (inside /auth/register route)
hashed_password = generate_password_hash(password)
```
The `/auth/register` endpoint receives an email and password. Crucially, we **never store the plain text password**. We use `generate_password_hash` from `werkzeug.security` to create a secure hash of the password.

#### User Login and JWT Generation

```python
import jwt
import datetime

# ... (inside /auth/login route)
user_to_login = ... # Find user by email
if user_to_login and check_password_hash(user_to_login["password"], password):
    token = jwt.encode({
        'user_id': user_to_login['id'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({"token": token})
```
The `/auth/login` endpoint validates the email and password. It uses `check_password_hash` to securely compare the provided password against the stored hash.

If successful, it generates a **JSON Web Token (JWT)**. The token's payload contains the user's ID and an **expiration date (`exp`)**, which we set to 30 minutes. The token is signed with our `SECRET_KEY`.

#### Protecting Routes with a Decorator

We need a way to ensure that only authenticated users can access certain routes. We achieve this with a reusable Python decorator: `@require_auth`.

```python
from functools import wraps
from flask import request, jsonify, g

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers and request.headers['Authorization'].startswith('Bearer '):
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({"error": "Authentication token is missing!"}), 401

        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            g.current_user = users.get(payload['user_id'])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return jsonify({"error": "Invalid or expired token!"}), 401

        return f(*args, **kwargs)
    return decorated_function

@app.route("/api/protected")
@require_auth
def protected_route():
    # Access the user's data via g.current_user
    return jsonify({"message": f"Hello, {g.current_user['email']}!"})
```
**How it works:**
1.  A decorator is a function that wraps another function, extending its behavior.
2.  `@require_auth` intercepts incoming requests to the `/api/protected` route.
3.  It extracts the token from the `Authorization: Bearer <token>` header.
4.  It uses `jwt.decode()` to validate the token's signature and expiration date.
5.  If valid, it attaches the user's data to Flask's global `g` object, making it accessible for the duration of the request.
6.  If the token is missing, invalid, or expired, it returns a `401 Unauthorized` error, blocking access to the route.

### 5. Run the Backend Server

```bash
# Make sure you are in the server/ directory and your venv is active
flask run --port 5001
```
Your Flask API is now running at `http://localhost:5001`.

---

## Frontend Setup (React)

Now, let's build the client-side interface to interact with our API.

### 1. Set Up the React Project

Navigate to the `client` directory. First, create a `package.json` file to manage your dependencies.

**`client/package.json`:**
```json
{
  "name": "client",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  },
  "browserslist": {
    "production": [">0.2%", "not dead", "not op_mini all"],
    "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
  }
}
```

### 2. Install Dependencies

```bash
# Navigate to the client directory
cd client

# Install the packages
npm install
```

### 3. The React Application Code

#### API Utility (`src/api.js`)
To keep our code organized, we centralize all API fetch logic in this file. It provides functions like `loginUser`, `registerUser`, and `getProtectedData`.

#### Main Component (`src/App.jsx`)
This component manages the entire user experience.

**State Management:**
```jsx
import React, { useState, useEffect } from 'react';

const [token, setToken] = useState(localStorage.getItem('token'));
// ... other state variables for form inputs, errors, etc.
```
- We use the `useState` hook to manage our component's state.
- The `token` is initialized from `localStorage`. This allows the app to "remember" the user's session if they refresh the page.

**Storing the Token:**
```jsx
useEffect(() => {
    if (token) {
        localStorage.setItem('token', token);
    } else {
        localStorage.removeItem('token');
    }
}, [token]);
```
- The `useEffect` hook syncs the `token` state with `localStorage`. When `token` changes, this effect runs, ensuring the token is always stored correctly.

**Making Authenticated Requests:**
```jsx
// From api.js
export const getProtectedData = (token) => {
    return fetch(`${API_BASE_URL}/api/protected`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`, // The JWT is sent here!
        },
    }).then(handleResponse);
};
```
When fetching protected data, we include the JWT in the `Authorization` header with the `Bearer` scheme. This is how our Flask backend will authenticate the request.

**Handling Authentication Errors:**
```jsx
// Inside App.jsx's handleFetchProtectedData
} catch (err) {
    setError(err.message);
    // If token is bad, log the user out
    if (err.message.includes('expired') || err.message.includes('Invalid')) {
        handleLogout();
    }
}
```
A crucial piece of logic: if the API returns an error indicating the token is expired or invalid (which our backend sends with a `401` status), we automatically log the user out by clearing the token from the state.

### 4. Run the Frontend Server

```bash
# Make sure you are in the client/ directory
npm start
```
Your React application is now running at `http://localhost:3000`.

---

## Running the Application

To run the full-stack application, you need to have both servers running simultaneously in two separate terminal windows:
1.  **Terminal 1 (Backend):** `cd server` -> `flask run --port 5001`
2.  **Terminal 2 (Frontend):** `cd client` -> `npm start`

Now, open `http://localhost:3000` in your browser. You can register a new user, log in, and fetch data from the protected backend route.

---

## Security Best Practices

- **Short-Lived Tokens:** The JWTs in this tutorial expire in 30 minutes. This is a good practice. Short-lived access tokens limit the damage if a token is compromised. For longer sessions, you would implement a refresh token flow.

- **`localStorage` and XSS:** Storing JWTs in `localStorage` is common but makes your application vulnerable to Cross-Site Scripting (XSS) attacks. If a malicious script runs on your site, it can steal the token from `localStorage`.

- **Production Recommendation: `HttpOnly` Cookies:** For production applications, a more secure method is to store the JWT in an `HttpOnly` cookie. `HttpOnly` cookies are not accessible to JavaScript, which mitigates XSS risks. This requires additional backend and frontend configuration to handle.

- **Always Use HTTPS:** In production, always serve your application over HTTPS to encrypt all communication between the client and server, protecting tokens and other data from being intercepted.
