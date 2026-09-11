"""
Application entry point.

This file used to hold every route directly. Now it only builds the
Flask app and registers blueprints — routes/pages.py and
routes/products.py hold the actual logic. As Luxora v2 grows (auth in
Phase 2, cart in Phase 3, orders in Phase 4), each of those becomes its
own blueprint here, instead of this file growing without bound.

Nothing about how the app behaves has changed: same routes, same
responses, same port. Run it exactly the same way you always have:
    python app.py
"""

from flask import Flask
from flask_cors import CORS

from config import Config
from routes.pages import pages
from routes.products import products_api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Kept for now, same as the original — see the audit note on why
    # this is likely safe to remove once confirmed nothing needs it.
    CORS(app)

    app.register_blueprint(pages)
    app.register_blueprint(products_api)

    return app


app = create_app()

if __name__ == "__main__":
    print(f"🚀 LUXORA Backend is running on http://localhost:{Config.PORT}")
    app.run(port=Config.PORT, debug=Config.DEBUG)
