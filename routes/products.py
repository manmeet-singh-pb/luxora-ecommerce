"""
Product API routes.

GET /api/products is unchanged in behavior and response shape from the
original app.py — same grouping by category, same fields. The frontend
(script.js, products.js) doesn't need to know this moved.
"""

from flask import Blueprint, jsonify

from db import get_db_connection

products_api = Blueprint("products_api", __name__)

# Known categories, seeded up front so the frontend always gets these
# keys even if a category currently has zero products (this matches
# the original behavior exactly).
KNOWN_CATEGORIES = ["shoes", "electronics", "clothing", "books", "home"]


@products_api.route("/api/products", methods=["GET"])
def get_products():
    conn = get_db_connection()
    db_products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()

    formatted_products = {category: [] for category in KNOWN_CATEGORIES}

    for row in db_products:
        cat = row["category"]
        if cat not in formatted_products:
            formatted_products[cat] = []  # safety net for an unseen category

        formatted_products[cat].append({
            "id": row["id"],
            "name": row["name"],
            "price": row["price"],
            "description": row["description"],
            "emoji": row["emoji"],
        })

    return jsonify(formatted_products)
