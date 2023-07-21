import json
import logging
from contextlib import contextmanager
from typing import List

import psycopg2
from backoff import backoff
from elasticsearch import Elasticsearch, helpers
from extract import Extract
from load import Load
from psycopg2.extras import DictCursor
from settings import get_settings
from state.state import State

from transform import transform

QUERY_PATH = "/postgres_to_es/updates_query.sql"


class ETL:
    def __init__(self) -> None:
        logging.info("Setting connections to PostgreSQL, Redis and Elasticsearch")
        self.extract = Extract()
        self.state = State()
        self.load = Load()

    def try_start(self) -> None:
        """Starts ETL process if another process is not running."""
        if self.state.is_running():
            logging.warning("Another process is running")
        else:
            self.state.set_running()
            self.__start()
            self.state.set_finished()

    def __start(self) -> None:
        """Extracts data from PostgreSQL,
        transforms it to bulk query, loads into Elasticsearch."""
        etl_state = self.state.get_etl_state()
        params = {"etl_state": etl_state}
        for batch in self.extract.iterbatches(params):
            bulk_query = transform(batch)
            self.load.bulk(bulk_query)

            last_row = batch[-1]
            self.state.set_etl_state(last_row["modified"])
