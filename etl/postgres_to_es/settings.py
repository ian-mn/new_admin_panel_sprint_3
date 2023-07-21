from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, Field


class RedisSettings(BaseSettings):
    host: Optional[str] = Field(None, env="redis_host")
    port: Optional[str] = Field(None, env="redis_port")
    password: Optional[str] = Field(None, env="redis_pass")


class PGSettings(BaseSettings):
    host: Optional[str] = Field(None, env="pg_host")
    port: Optional[str] = Field(None, env="pg_port")
    password: Optional[str] = Field(None, env="pg_pass")
    user: Optional[str] = Field(None, env="pg_user")
    dbname: Optional[str] = Field(None, env="pg_db")


class ESSettings(BaseSettings):
    host: Optional[str] = Field(None, env="elastic_host")
    port: Optional[str] = Field(None, env="elastic_port")


class Settings(BaseSettings):
    redis: RedisSettings = RedisSettings()
    pg: PGSettings = PGSettings()
    es: ESSettings = ESSettings()
    batch_size: int = Field(None, env="batch_size")
    use_redis_storage: bool = Field(True, env="use_redis_storage")


@lru_cache
def get_settings() -> Settings:
    return Settings()
