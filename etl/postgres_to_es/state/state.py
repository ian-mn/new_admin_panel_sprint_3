import abc
import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict

from backoff import backoff
from redis import Redis
from settings import get_settings
from state.storage import JSONStorage, RedisStorage


class State:
    """Provides methods to get and set key, value pair of string and datetime converted to string."""

    DEFAULT_VALUE = datetime(2023, 5, 1, 0, 0, 0, 0, timezone.utc)
    IS_RUNNING_KEY = "is_running"
    ETL_STATE_KEY = "etl_state"

    def __init__(self) -> None:
        if get_settings().use_redis_storage:
            self.storage = RedisStorage()
        else:
            self.storage = JSONStorage()

    def get_etl_state(self) -> str:
        """Gets ETL state value from storage.
        If key doesn't exist, returns default date.

        Returns:
            str: datetime converted to string.
        """
        value = self.storage.get(self.ETL_STATE_KEY)
        if value:
            return value
        return str(self.DEFAULT_VALUE)

    def set_etl_state(self, value: datetime) -> None:
        """Sets value to a ETL state key. Value is converted to string.

        Args:
            value (datetime): Datetime value.

        Raises:
            ValueError: if key is not string or value is not datetime raises exception.
        """
        if type(value) != datetime:
            raise ValueError
        self.storage.set(self.ETL_STATE_KEY, str(value))

    def is_running(self) -> bool:
        status = self.storage.get(self.IS_RUNNING_KEY)
        if status:
            return status == "True"
        return False

    def set_running(self):
        self.storage.set(self.IS_RUNNING_KEY, "True")

    def set_finished(self):
        self.storage.set(self.IS_RUNNING_KEY, "False")
