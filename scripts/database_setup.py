import sqlite3
import os

DB_FILE = "database.db"

# Remove the old database file if it exists to start fresh
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print("Old database removed.")

# Connect to the SQLite database
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Enable foreign key support, which is crucial for data integrity
cursor.execute("PRAGMA foreign_keys = ON;")

# --- Table Creation ---

# 1. roles table
cursor.execute(
    """
CREATE TABLE roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT NOT NULL UNIQUE
)
"""
)

# 2. users table
cursor.execute(
    """
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role_id INTEGER,
    FOREIGN KEY(role_id) REFERENCES roles(role_id)
)
"""
)

# 3. countries table
cursor.execute(
    """
CREATE TABLE countries (
    country_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_name TEXT NOT NULL UNIQUE
)
"""
)

# 4. vacations table
cursor.execute(
    """
CREATE TABLE vacations (
    vacation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id INTEGER,
    description TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    price REAL NOT NULL,
    image_file_name TEXT,
    FOREIGN KEY(country_id) REFERENCES countries(country_id)
)
"""
)

# 5. likes table (join table for many-to-many relationship between users and vacations)
cursor.execute(
    """
CREATE TABLE likes (
    user_id INTEGER,
    vacation_id INTEGER,
    PRIMARY KEY (user_id, vacation_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (vacation_id) REFERENCES vacations(vacation_id) ON DELETE CASCADE
)
"""
)

# --- Data Insertion ---

# Insert roles
cursor.execute("INSERT INTO roles (role_name) VALUES ('Admin')")
cursor.execute("INSERT INTO roles (role_name) VALUES ('User')")

# Insert users
cursor.execute(
    "INSERT INTO users (first_name, last_name, email, password, role_id) VALUES ('Admin', 'Admin', 'admin@vacations.com', 'admin123', 1)"
)
cursor.execute(
    "INSERT INTO users (first_name, last_name, email, password, role_id) VALUES ('John', 'Doe', 'john.doe@email.com', 'user1234', 2)"
)
cursor.execute(
    "INSERT INTO users (first_name, last_name, email, password, role_id) VALUES ('Jane', 'Smith', 'jane.smith@email.com', 'pass5678', 2)"
)

# Insert countries
countries = [
    ("USA",),
    ("Spain",),
    ("Italy",),
    ("Greece",),
    ("Thailand",),
    ("Japan",),
    ("France",),
    ("Australia",),
    ("Brazil",),
    ("Canada",),
]
cursor.executemany("INSERT INTO countries (country_name) VALUES (?)", countries)

# Insert vacations with country_id values
vacations = [
    (1, "Sunny beach vacation in Miami", "2025-07-10", "2025-07-20", 2500, "miami.jpg"),
    (2, "Explore the history of Barcelona", "2025-08-01", "2025-08-10", 1800, "barcelona.jpg"),
    (3, "Romantic getaway in Rome", "2025-09-05", "2025-09-12", 3000, "rome.jpg"),
    (4, "Island hopping in the Greek isles", "2025-06-15", "2025-06-25", 4500, "greece.jpg"),
    (5, "Adventure in Bangkok", "2025-11-20", "2025-11-30", 2200, "bangkok.jpg"),
    (6, "Cultural tour of Kyoto", "2026-04-10", "2026-04-20", 5000, "kyoto.jpg"),
    (7, "Visit the Eiffel Tower in Paris", "2025-10-01", "2025-10-07", 2800, "paris.jpg"),
    (8, "Outback adventure in Sydney", "2026-01-15", "2026-01-25", 6000, "sydney.jpg"),
    (9, "Carnival in Rio de Janeiro", "2026-02-20", "2026-02-28", 3500, "rio.jpg"),
    (10, "Skiing in the Canadian Rockies", "2025-12-10", "2025-12-18", 4000, "canada.jpg"),
    (1, "New York City sightseeing", "2025-05-20", "2025-05-27", 3200, "nyc.jpg"),
    (2, "Andalusian tour in Seville", "2025-09-15", "2025-09-22", 1900, "seville.jpg"),
]

cursor.executemany(
    "INSERT INTO vacations (country_id, description, start_date, end_date, price, image_file_name) VALUES (?, ?, ?, ?, ?, ?)",
    vacations,
)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database setup complete.")