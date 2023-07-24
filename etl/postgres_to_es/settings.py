from functools import lru_cache

from pydantic import BaseSettings, Field


class RedisSettings(BaseSettings):
    host: str | None = Field(None, env="redis_host")
    port: str | None = Field(None, env="redis_port")
    password: str | None = Field(None, env="redis_pass")


class PGSettings(BaseSettings):
    host: str | None = Field(None, env="pg_host")
    port: str | None = Field(None, env="pg_port")
    password: str | None = Field(None, env="pg_pass")
    user: str | None = Field(None, env="pg_user")
    dbname: str | None = Field(None, env="pg_db")


class ESSettings(BaseSettings):
    host: str | None = Field(None, env="elastic_host")
    port: str | None = Field(None, env="elastic_port")


class Settings(BaseSettings):
    redis: RedisSettings = RedisSettings()
    pg: PGSettings = PGSettings()
    es: ESSettings = ESSettings()
    batch_size: int = Field(None, env="batch_size")
    use_redis_storage: bool = Field(True, env="use_redis_storage")
    automatic_updates: bool = Field(True, env="automatic_updates")


@lru_cache
def get_settings() -> Settings:
    return Settings()
