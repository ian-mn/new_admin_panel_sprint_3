import logging
from contextlib import contextmanager

import psycopg2
from backoff import backoff_generator
from logger import logger
from psycopg2.extras import DictCursor
from settings import get_settings


class Extract:
    QUERY_PATH = "queries/updates_query.sql"

    def __init__(self) -> None:
        self.pg = get_settings().pg
        self.batch_size = get_settings().batch_size

    @contextmanager
    def __conn_context(self):
        """PostgreSQL connection context manager."""
        conn = psycopg2.connect(**self.pg.dict(), cursor_factory=DictCursor)
        psycopg2.extras.register_uuid()
        yield conn
        conn.close()

    @backoff_generator()
    def iterbatches(self, params: dict):
        """Yields batch from specified table and update date.

        Args:
            params (dict): Dictionary with table name and table state.
        """
        with self.__conn_context() as conn:
            logger.info(f"Extracting from PostgreSQL with params: {params}")
            curs = conn.cursor()
            query = self.__parametrize_query(self.QUERY_PATH, params)
            curs.execute(query)
            while True:
                rows = curs.fetchmany(self.batch_size)
                logger.info(f"Extracted {len(rows)} rows.")
                if not rows:
                    break
                yield rows

    def __parametrize_query(self, query_path: str, params: dict) -> str:
        """Opens sql query and replaces parameters based on params dictionary.

        Args:
            query_path (str): Query path.
            params (dict): Replace key with value in a query.

        Returns:
            str: Query with parameters.
        """
        with open(query_path, "r") as f:
            query = f.read()
            for key, value in params.items():
                query = query.replace(key, value)
            return query
