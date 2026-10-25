import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load local settings from nripmc-website/.env when it exists.
load_dotenv(PROJECT_ROOT / ".env")

DATABASE_PATH = PROJECT_ROOT / "instance" / "nripmc.sqlite3"


class Config:
    # Set SESSION_SECRET in your .env file before starting the website.
    SECRET_KEY = os.environ.get("SESSION_SECRET")

    # Use DATABASE_URL if you later choose a different database.
    # Otherwise, keep the initial development database in instance/.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{DATABASE_PATH.as_posix()}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CSRF protection will be enabled for forms in a later step.
    WTF_CSRF_ENABLED = True

    # Local HTTP development can use false; set true when running behind HTTPS.
    SESSION_COOKIE_SECURE = (
        os.environ.get("SESSION_COOKIE_SECURE", "false").strip().lower() == "true"
    )
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    REMEMBER_COOKIE_SECURE = SESSION_COOKIE_SECURE
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"