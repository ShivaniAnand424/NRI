import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from database import create_database_engine, metadata


load_dotenv()
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///{(Path(__file__).parent / 'nripmc.db').as_posix()}",
)
_engine = create_database_engine(DATABASE_URL)


def get_conn():
    return _engine.connect()


def init_db():
    metadata.create_all(_engine)


def create_user(full_name, email, phone, country, password_hash):
    """Returns True if saved, False if the email already exists."""
    try:
        with _engine.begin() as conn:
            conn.execute(
                text(
                    """
                    INSERT INTO users (full_name, email, phone, country, password_hash)
                    VALUES (:full_name, :email, :phone, :country, :password_hash)
                    """
                ),
                {
                    "full_name": full_name,
                    "email": email,
                    "phone": phone or "",
                    "country": country or "",
                    "password_hash": password_hash,
                },
            )
        return True
    except IntegrityError:
        return False


def get_user_by_email(email):
    with _engine.connect() as conn:
        return conn.execute(
            text("SELECT * FROM users WHERE email = :email"),
            {"email": email},
        ).mappings().first()


def get_user_by_id(user_id):
    with _engine.connect() as conn:
        return conn.execute(
            text("SELECT * FROM users WHERE id = :user_id"),
            {"user_id": user_id},
        ).mappings().first()
