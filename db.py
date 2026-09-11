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
