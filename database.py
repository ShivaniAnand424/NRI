"""Database layer for the NRIPMC website (Aiven for MySQL, SQLite as local fallback)."""
import os
from pathlib import Path

import pymysql
from dotenv import load_dotenv
from flask import g
from pymysql.cursors import DictCursor
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, make_url

PROJECT_DIR = Path(__file__).resolve().parent
load_dotenv(PROJECT_DIR / ".env")


def _ca_path():
    configured = os.environ.get("DB_SSL_CA")
    candidates = []

    if configured:
        ca = Path(configured)
        candidates.append(ca if ca.is_absolute() else PROJECT_DIR / ca)

    candidates.extend((PROJECT_DIR / "certs" / "ca.pem", Path("/etc/secrets/ca.pem")))

    for ca in candidates:
        if ca.is_file():
            return str(ca)

    raise FileNotFoundError(
        "MySQL CA certificate not found. Set DB_SSL_CA to the certificate path; "
        "on Render, add it as a Secret File and use /etc/secrets/ca.pem."
    )


def connect():
    """Plain PyMySQL connection (used by check_setup.py)."""
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ.get("DB_PORT", "3306")),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ.get("DB_NAME", "defaultdb"),
        charset="utf8mb4",
        cursorclass=DictCursor,
        connect_timeout=10,
        ssl={"ca": _ca_path(), "check_hostname": False},
    )


MYSQL_SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        full_name VARCHAR(200) NOT NULL,
        email VARCHAR(190) NOT NULL UNIQUE,
        phone VARCHAR(50) NOT NULL DEFAULT '',
        country VARCHAR(100) NOT NULL DEFAULT '',
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
    """
    CREATE TABLE IF NOT EXISTS service_enquiries (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        service_slug VARCHAR(100) NOT NULL,
        responses_json TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_service_enquiries_user (user_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
    """
    CREATE TABLE IF NOT EXISTS enquiries (
        id INT AUTO_INCREMENT PRIMARY KEY,
        full_name VARCHAR(200) NOT NULL,
        contact VARCHAR(255) NOT NULL,
        property_location VARCHAR(255) NOT NULL DEFAULT '',
        service VARCHAR(150) NOT NULL DEFAULT '',
        requirement TEXT NOT NULL,
        source_page VARCHAR(255) NOT NULL DEFAULT '',
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
]

SQLITE_SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT NOT NULL DEFAULT '',
        country TEXT NOT NULL DEFAULT '',
        password_hash TEXT NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS service_enquiries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        service_slug TEXT NOT NULL,
        responses_json TEXT NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS enquiries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        contact TEXT NOT NULL,
        property_location TEXT NOT NULL DEFAULT '',
        service TEXT NOT NULL DEFAULT '',
        requirement TEXT NOT NULL,
        source_page TEXT NOT NULL DEFAULT '',
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """,
]


def _build_url(app):
    if os.environ.get("DB_HOST"):
        return URL.create(
            "mysql+pymysql",
            username=os.environ.get("DB_USER", "avnadmin"),
            password=os.environ.get("DB_PASSWORD", ""),
            host=os.environ["DB_HOST"],
            port=int(os.environ.get("DB_PORT", "3306")),
            database=os.environ.get("DB_NAME", "defaultdb"),
        )
    url = make_url(app.config["DATABASE_URL"])
    if url.get_backend_name() == "mysql":
        url = url.set(drivername="mysql+pymysql", query={})
    return url


def init_app(app):
    url = _build_url(app)
    options = {"pool_pre_ping": True, "pool_recycle": 280}

    if url.get_backend_name() == "mysql":
        options["connect_args"] = {"ssl": {"ca": _ca_path(), "check_hostname": False}}
        schema = MYSQL_SCHEMA
    else:
        schema = SQLITE_SCHEMA

    engine = create_engine(url, **options)
    app.extensions["db_engine"] = engine

    with engine.begin() as conn:
        for statement in schema:
            conn.execute(text(statement))


def get_db():
    """One connection per request; app.py closes it in teardown_appcontext."""
    if "db" not in g:
        from flask import current_app

        g.db = current_app.extensions["db_engine"].connect()
    return g.db