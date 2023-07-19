"""PostgreSQL loader."""
from enum import Enum
from typing import List

import psycopg2
from log import logger
from models.tables import Row
from psycopg2.extras import execute_values


class InsertType(Enum):
    INSERT = ""
    UPSERT = "ON CONFLICT (id) DO NOTHING"


class PostgresLoader:
    def __init__(self, conn, how=InsertType.UPSERT) -> None:
        self.conn = conn
        self.how = how

    def load(self, rows: List[Row]):
        """Loads list of Rows to PostgreSQL.

        Args:
            rows (List[Row]): rows to load
        """
        fisrt_row = rows[0]
        keys_str = self.__get_keys_str(fisrt_row)
        target_name = fisrt_row.target_name
        values = [list(x.__dict__.values()) for x in rows]

        query = f"""
            INSERT INTO {target_name} ({keys_str})
            VALUES %s
            {self.how.value};
        """

        curs = self.conn.cursor()

        try:
            execute_values(curs, query, values)
            self.conn.commit()
        except psycopg2.Error as e:
            logger.error("PostgreSQL error: %s" % (" ".join(e.args)))
            self.conn.close()

    def __get_keys_str(self, first_row: Row) -> str:
        """Generates keys separated by commas from Row.

        Args:
            first_row (Row): First row

        Returns:
            str: Keys separated by commas
        """
        keys = list(first_row.__dict__.keys())
        return ",".join(keys)
