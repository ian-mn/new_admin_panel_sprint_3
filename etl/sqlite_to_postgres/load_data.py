"""Loads data from SQLite to PostgreSQL."""
import sqlite3

import backoff
import psycopg2
from config import get_settings
from connections import pg_conn_context, sqlite_conn_context
from log import logger
from models.tables import get_models
from postgres_loader import InsertType, PostgresLoader
from psycopg2.extensions import connection as _connection
from sqlite_extractor import SQLiteExtractor


def load_from_sqlite(
    sqlite_conn: sqlite3.Connection,
    pg_conn: _connection,
    batch_size=50,
    how=InsertType.UPSERT,
) -> None:
    """Основной метод загрузки данных из SQLite в Postgres"""

    sqlite_extractor = SQLiteExtractor(sqlite_conn, batch_size)
    postgres_loader = PostgresLoader(pg_conn, how)

    models = get_models()

    for model in models:
        for batch in sqlite_extractor.extract(model):
            postgres_loader.load(batch)


@backoff.on_exception(backoff.expo, psycopg2.Error)
def main():
    logger.info("Transfer between SQLite to PostgreSQL started.")
    settings = get_settings()
    with sqlite_conn_context() as sqlite_conn, pg_conn_context() as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn, batch_size=settings.batch_size)


if __name__ == "__main__":
    main()
