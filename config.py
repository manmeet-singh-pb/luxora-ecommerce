"""
Central place for all configuration.

Nothing here is secret by itself — the point is that every value that
*could* change between your laptop, a teammate's laptop, and a real
deployment lives in one place and is read from the environment instead
of being hardcoded across the codebase.

For local development, values fall back to sane defaults so the app
still runs with zero setup. A real deployment would set these as actual
environment variables (or via a .env file — see .env.example).
"""

import os

# python-dotenv loads a local .env file into os.environ if one exists.
# It's optional in production (real env vars would already be set there),
# which is why we don't fail if the package or file is missing.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Config:
    # Where the SQLite file lives. Kept configurable so tests or a
    # deployment can point at a different path without touching code.
    DATABASE_PATH = os.environ.get("DATABASE_PATH", "luxora.db")

    # Used by Flask to sign session cookies. Not used yet (Phase 1 has
    # no auth), but it's wired up now so Phase 2 doesn't need another
    # config pass. NEVER commit a real value — see .env.example.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")

    # Standard Flask debug flag. Off by default — has to be explicitly
    # turned on via FLASK_DEBUG=1 in your environment.
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

    PORT = int(os.environ.get("PORT", 5001))
