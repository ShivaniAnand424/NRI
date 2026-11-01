import os
from threading import Lock

from flask import current_app, g
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    UniqueConstraint,
    create_engine,
    func,
)


metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("full_name", String(255), nullable=False),
    Column("email", String(320), nullable=False),
    Column("phone", String(100), nullable=False, server_default=""),
    Column("country", String(100), nullable=False, server_default=""),
    Column("password_hash", String(255), nullable=False),
    UniqueConstraint("email"),
    mysql_engine="InnoDB",
    mysql_charset="utf8mb4",
    mysql_collate="utf8mb4_unicode_ci",
)

service_enquiries = Table(
    "service_enquiries",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, nullable=False),
    Column("service_slug", String(100), nullable=False),
    Column("responses_json", Text, nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=func.current_timestamp()),
    mysql_engine="InnoDB",
    mysql_charset="utf8mb4",
    mysql_collate="utf8mb4_unicode_ci",
)

enquiries = Table(
    "enquiries",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("full_name", String(255), nullable=False),
    Column("contact", String(320), nullable=False),
    Column("property_location", String(500), nullable=False, server_default=""),
    Column("service", String(255), nullable=False, server_default=""),
    Column("requirement", Text, nullable=False),
    Column("source_page", String(200), nullable=False, server_default=""),
    Column("created_at", DateTime, nullable=False, server_default=func.current_timestamp()),
    mysql_engine="InnoDB",
    mysql_charset="utf8mb4",
    mysql_collate="utf8mb4_unicode_ci",
)


def create_database_engine(database_url):
    return create_engine(
        database_url,
        pool_pre_ping=database_url.startswith("mysql"),
    )


def init_app(app):
    database_url = app.config["DATABASE_URL"]
    app.extensions["database_engine"] = create_database_engine(database_url)
    app.extensions["database_schema_lock"] = Lock()
    app.extensions["database_schema_initialized"] = False


def get_db():
    if "db" not in g:
        engine = current_app.extensions["database_engine"]
        if not current_app.extensions["database_schema_initialized"]:
            with current_app.extensions["database_schema_lock"]:
                if not current_app.extensions["database_schema_initialized"]:
                    metadata.create_all(engine)
                    current_app.extensions["database_schema_initialized"] = True
        g.db = engine.connect()
    return g.db
