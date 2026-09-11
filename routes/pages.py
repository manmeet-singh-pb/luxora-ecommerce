"""
Page routes: everything that renders an HTML template.

This is the same allow-list pattern from the original app.py, just
moved into its own blueprint. That pattern was already a good security
habit (it stops someone requesting arbitrary files from templates/ via
the URL) — Phase 1 preserves it as-is rather than "improving" something
that wasn't broken.
"""

from flask import Blueprint, render_template

pages = Blueprint("pages", __name__)

ALLOWED_PAGES = {"index.html", "products.html", "cart.html", "login.html"}


@pages.route("/")
def home():
    return render_template("index.html")


@pages.route("/<page_name>")
def serve_page(page_name):
    if page_name in ALLOWED_PAGES:
        return render_template(page_name)
    return "Page not found", 404
