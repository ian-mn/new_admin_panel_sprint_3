"""SQLite extractor.."""
import sqlite3
from typing import List

from log import logger
from models.tables import Row


class SQLiteExtractor:
    def __init__(self, conn, batch_size=50):
        self.conn = conn
        self.batch_size = batch_size

    def extract(self, model: Row):
        """Extracts batch of Rows from SQLite.

        Args:
            model (Row): what table to read

        Yields:
            _type_: batch of rows
        """
        curs = self.conn.cursor()

        try:
            curs.execute(f"SELECT * FROM {model.source_name}")
        except sqlite3.Error as e:
            logger.error("SQLite error: %s" % (" ".join(e.args)))
            self.conn.close()

        while True:
            rows = curs.fetchmany(self.batch_size)
            if not rows:
                return
            batch = self.rows_to_model(rows, model)
            yield batch

    def rows_to_model(self, rows, model) -> List[Row]:
        """Converts SQLite Rows to list of Rows

        Args:
            rows (_type_): SQLite Rows
            model (_type_): Model

        Returns:
            List[Row]: List of Rows
        """
        models = []
        for row in rows:
            row_dict = {key: value for key, value in zip(row.keys(), row)}
            models.append(model.from_dict(row_dict))
        return models
