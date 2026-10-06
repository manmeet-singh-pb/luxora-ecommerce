"""
Database connection helper.

This is exactly the pattern that was already living inline in app.py —
pulled out into its own module so every blueprint can import it instead
of duplicating the connect/row_factory boilerplate. No behavior change.
"""

import sqlite3

from config import Config


def get_db_connection():
    """Open a new SQLite connection with dict-like row access.

    A fresh connection per request is the right call at this scale —
    SQLite connections are cheap and this avoids any cross-request
    state or threading surprises. If Luxora ever needs connection
    pooling, that's a Phase 7 concern, not now.
    """
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # access columns by name, e.g. row['price']
    return conn


def ensure_tables():
    """Create all required tables if they don't already exist.

    Safe to call on every app startup — CREATE TABLE IF NOT EXISTS
    is a no-op when the table is already present, so existing data
    (products, users) is never touched.
    """
    conn = get_db_connection()
    try:
        # Existing products table — schema matches setup_db.py exactly.
        conn.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                name TEXT,
                price REAL,
                description TEXT,
                emoji TEXT
            )
        ''')
        # Users table — added in Phase 2 for real authentication.
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
    finally:
        conn.close()
