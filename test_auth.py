"""
Phase 2 authentication tests.

Run with: python test_auth.py

Uses Flask's built-in test client — no extra dependencies needed.
A temporary test database is created and cleaned up automatically.
"""

import os
import sys

# Use a separate test database so real data is never touched.
TEST_DB = "test_luxora.db"
if os.path.exists(TEST_DB):
    os.unlink(TEST_DB)
os.environ["DATABASE_PATH"] = TEST_DB

from app import create_app  # noqa: E402 — must set env before import
from db import get_db_connection  # noqa: E402


def run_tests():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    passed = 0
    failed = 0

    def check(name, condition):
        nonlocal passed, failed
        if condition:
            print(f"  PASS: {name}")
            passed += 1
        else:
            print(f"  FAIL: {name}")
            failed += 1

    # Seed a couple of test products
    conn = get_db_connection()
    conn.executemany(
        "INSERT INTO products (category, name, price, description, emoji) "
        "VALUES (?, ?, ?, ?, ?)",
        [
            ("shoes", "Test Shoe", 5999, "A test shoe", "S"),
            ("electronics", "Test Watch", 9999, "A test watch", "W"),
        ],
    )
    conn.commit()
    conn.close()

    # ---- Basic pages ----
    print("\n--- Basic pages ---")
    r = client.get("/")
    check("Homepage returns 200", r.status_code == 200)

    r = client.get("/api/products")
    check("Products API returns 200", r.status_code == 200)
    data = r.get_json()
    check("Products API returns categories", "shoes" in data)
    total = sum(len(v) for v in data.values())
    check(f"Products data intact ({total} products)", total == 2)

    # ---- Unauthenticated ----
    print("\n--- Auth: unauthenticated ---")
    r = client.get("/api/auth/me")
    check("/api/auth/me returns 401 when not logged in", r.status_code == 401)

    # ---- Registration ----
    print("\n--- Auth: registration ---")
    r = client.post("/api/auth/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
    })
    check("Register returns 201", r.status_code == 201)
    data = r.get_json()
    check("Register returns user info", "user" in data)
    check("Register does not return password_hash",
          "password_hash" not in data.get("user", {}))

    # ---- Duplicate registration ----
    r = client.post("/api/auth/register", json={
        "name": "Another User",
        "email": "test@example.com",
        "password": "different456",
    })
    check("Duplicate email returns 409", r.status_code == 409)

    # ---- Auto-login after registration ----
    r = client.get("/api/auth/me")
    check("/api/auth/me returns 200 after registration (auto-login)",
          r.status_code == 200)

    # ---- Logout ----
    print("\n--- Auth: logout ---")
    r = client.post("/api/auth/logout")
    check("Logout returns 200", r.status_code == 200)

    r = client.get("/api/auth/me")
    check("/api/auth/me returns 401 after logout", r.status_code == 401)

    # ---- Login with correct credentials ----
    print("\n--- Auth: login ---")
    r = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "password123",
    })
    check("Login returns 200 with correct credentials", r.status_code == 200)
    data = r.get_json()
    check("Login returns user name",
          data.get("user", {}).get("name") == "Test User")
    check("Login returns user email",
          data.get("user", {}).get("email") == "test@example.com")

    r = client.get("/api/auth/me")
    check("/api/auth/me returns 200 after login", r.status_code == 200)

    # ---- Login with wrong credentials ----
    print("\n--- Auth: invalid credentials ---")
    client.post("/api/auth/logout")
    r = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "wrongpassword",
    })
    check("Login with wrong password returns 401", r.status_code == 401)
    check(
        "Error message is generic (doesn't reveal which field is wrong)",
        "Invalid email or password" in r.get_json().get("error", ""),
    )

    r = client.post("/api/auth/login", json={
        "email": "nobody@example.com",
        "password": "password123",
    })
    check("Login with non-existent email returns 401", r.status_code == 401)

    # ---- Password security ----
    print("\n--- Security ---")
    conn = get_db_connection()
    user = conn.execute(
        "SELECT password_hash FROM users WHERE email = ?",
        ("test@example.com",),
    ).fetchone()
    conn.close()
    check(
        "Password is stored as hash (not plaintext)",
        user is not None
        and user["password_hash"] != "password123"
        and len(user["password_hash"]) > 50,
    )

    # ---- Validation ----
    print("\n--- Validation ---")
    r = client.post("/api/auth/register", json={
        "name": "", "email": "", "password": "",
    })
    check("Empty fields rejected (400)", r.status_code == 400)

    r = client.post("/api/auth/register", json={
        "name": "X", "email": "not-an-email", "password": "12345678",
    })
    check("Invalid email rejected (400)", r.status_code == 400)

    r = client.post("/api/auth/register", json={
        "name": "X", "email": "x@x.com", "password": "short",
    })
    check("Short password rejected (400)", r.status_code == 400)

    # ---- Email normalization ----
    print("\n--- Email normalization ---")
    r = client.post("/api/auth/register", json={
        "name": "Upper Case", "email": "UPPER@EXAMPLE.COM",
        "password": "password123",
    })
    check("Registration normalizes email to lowercase", r.status_code == 201)
    data = r.get_json()
    check("Returned email is lowercase",
          data.get("user", {}).get("email") == "upper@example.com")

    # ---- Products still intact ----
    print("\n--- Data integrity ---")
    r = client.get("/api/products")
    data = r.get_json()
    total = sum(len(v) for v in data.values())
    check(f"Product data still intact after auth operations ({total} products)",
          total == 2)

    # ---- Summary ----
    print(f"\n{'=' * 50}")
    print(f"  Results: {passed} passed, {failed} failed, {passed + failed} total")
    print(f"{'=' * 50}")

    return failed == 0


if __name__ == "__main__":
    try:
        success = run_tests()
    finally:
        # Clean up the test database
        try:
            os.unlink(TEST_DB)
            print(f"\n  Cleaned up {TEST_DB}")
        except OSError:
            pass

    sys.exit(0 if success else 1)
