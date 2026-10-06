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
import secrets

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

    # Required for session security (Phase 2 authentication). If not
    # set, a random key is generated for development convenience —
    # sessions will NOT survive server restarts. For production, always
    # set SECRET_KEY in your .env file or environment.
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

    # Standard Flask debug flag. Off by default — has to be explicitly
    # turned on via FLASK_DEBUG=1 in your environment.
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

    PORT = int(os.environ.get("PORT", 5001))

    # Session cookie security settings.
    SESSION_COOKIE_HTTPONLY = True    # Prevent JavaScript access to session cookie
    SESSION_COOKIE_SAMESITE = "Lax"  # Protect against CSRF in most cases
