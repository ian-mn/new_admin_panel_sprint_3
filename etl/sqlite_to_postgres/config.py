"""Settings management"""
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings from .env file"""

    sqlite_path: str
    batch_size: int
    pg_user: str
    pg_pass: str
    pg_host: str
    pg_port: int
    pg_db: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """Returns settings generated from .env file.

    Returns:
        Settings: Settings
    """
    return Settings()
