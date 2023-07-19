"""Connections to DBs."""
import sqlite3
from contextlib import contextmanager

import psycopg2
from config import get_settings
from psycopg2.extras import DictCursor


@contextmanager
def sqlite_conn_context():
    """SQLite connection context manager.

    Yields:
        _type_: SQLite connection
    """
    settings = get_settings()
    conn = sqlite3.connect(settings.sqlite_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


@contextmanager
def pg_conn_context():
    """PostgreSQL cooection context manager.

    Yields:
        _type_: PostgreSQL connection
    """
    settings = get_settings()
    conn = psycopg2.connect(
        **{
            "dbname": settings.pg_db,
            "user": settings.pg_user,
            "password": settings.pg_pass,
            "host": settings.pg_host,
            "port": settings.pg_port,
        }
    )
    conn.cursor_factory = DictCursor
    yield conn
    conn.close()
