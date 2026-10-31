import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).parent / "nripmc.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with closing(get_conn()) as conn, conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name     TEXT NOT NULL,
                email         TEXT NOT NULL UNIQUE,
                phone         TEXT,
                country       TEXT,
                password_hash TEXT NOT NULL,
                created_at    TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def create_user(full_name, email, phone, country, password_hash):
    """Returns True if saved, False if the email already exists."""
    try:
        with closing(get_conn()) as conn, conn:
            conn.execute(
                "INSERT INTO users (full_name, email, phone, country, password_hash) "
                "VALUES (?, ?, ?, ?, ?)",
                (full_name, email, phone, country, password_hash),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def get_user_by_email(email):
    with closing(get_conn()) as conn:
        return conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()


def get_user_by_id(user_id):
    with closing(get_conn()) as conn:
        return conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()