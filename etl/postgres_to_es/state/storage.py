import abc
import json
from typing import Any

from backoff import backoff
from logger import logger
from redis import Redis
from settings import get_settings


class BaseStorage(abc.ABC):
    @abc.abstractmethod
    def get(self, key: str) -> Any:
        """Gets the state value by key."""

    @abc.abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Sets the state value by key."""


class RedisStorage(BaseStorage):
    def __init__(self) -> None:
        redis = get_settings().redis
        self.redis_adapter = Redis(
            **redis.dict(), charset="utf-8", decode_responses=True
        )

    @backoff()
    def get(self, key: str) -> Any:
        logger.info(f"Getting Redis {key}")
        return self.redis_adapter.get(key)

    @backoff()
    def set(self, key: str, value: Any) -> None:
        logger.info(f"Setting Redis {key} to {value}")
        self.redis_adapter.set(key, value)


class JSONStorage(BaseStorage):
    def __init__(self) -> None:
        self.file_path = "storage.json"

    def get(self, key: str) -> Any:
        data = self.__read_data()
        return data.get(key, None)

    def set(self, key: str, value: Any) -> None:
        data = self.__read_data()
        data[key] = value
        self.__save_data(data)

    def __read_data(self) -> dict[str, Any]:
        try:
            with open(self.file_path) as f:
                return json.load(f)
        except IOError:
            return {}

    def __save_data(self, data: dict[str, Any]) -> None:
        with open(self.file_path, "w") as f:
            json.dump(data, f)
