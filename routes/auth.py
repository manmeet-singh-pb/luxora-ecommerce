"""
Authentication routes (Phase 2).

Provides user registration, login, logout, and session checking.
Uses Flask's built-in session mechanism (server-side signed cookies)
and Werkzeug's password hashing utilities.
"""

import re

from flask import Blueprint, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db_connection

auth = Blueprint("auth", __name__)

# Simple email pattern — good enough for a portfolio project.
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@auth.route("/api/auth/register", methods=["POST"])
def register():
    """Create a new user account and log them in automatically."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    # --- validation ---
    if not name:
        return jsonify({"error": "Name is required."}), 400
    if len(name) > 100:
        return jsonify({"error": "Name is too long."}), 400
    if not email:
        return jsonify({"error": "Email is required."}), 400
    if not _EMAIL_RE.match(email):
        return jsonify({"error": "Please enter a valid email address."}), 400
    if len(email) > 255:
        return jsonify({"error": "Email is too long."}), 400
    if not password:
        return jsonify({"error": "Password is required."}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400

    conn = get_db_connection()
    try:
        existing = conn.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        ).fetchone()
        if existing:
            return jsonify({"error": "An account with this email already exists."}), 409

        password_hash = generate_password_hash(password)
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
        conn.commit()
        user_id = cursor.lastrowid

        # Auto-login after registration
        session.clear()
        session["user_id"] = user_id

        return jsonify({
            "message": "Registration successful.",
            "user": {"id": user_id, "name": name, "email": email},
        }), 201
    finally:
        conn.close()


@auth.route("/api/auth/login", methods=["POST"])
def login():
    """Authenticate an existing user and create a session."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    conn = get_db_connection()
    try:
        user = conn.execute(
            "SELECT id, name, email, password_hash FROM users WHERE email = ?",
            (email,),
        ).fetchone()

        # Generic error so attackers can't enumerate valid emails.
        if not user or not check_password_hash(user["password_hash"], password):
            return jsonify({"error": "Invalid email or password."}), 401

        session.clear()
        session["user_id"] = user["id"]

        return jsonify({
            "message": "Login successful.",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
            },
        })
    finally:
        conn.close()


@auth.route("/api/auth/logout", methods=["POST"])
def logout():
    """Clear the current session."""
    session.clear()
    return jsonify({"message": "Logged out successfully."})


@auth.route("/api/auth/me", methods=["GET"])
def me():
    """Return the currently authenticated user, or 401."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not authenticated."}), 401

    conn = get_db_connection()
    try:
        user = conn.execute(
            "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            # User was deleted or DB was reset — clear stale session.
            session.clear()
            return jsonify({"error": "Not authenticated."}), 401

        return jsonify({
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
            },
        })
    finally:
        conn.close()
