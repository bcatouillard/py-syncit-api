"""Settings module."""

from enum import StrEnum
from functools import lru_cache
from typing import Self

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    """ENUM Environments."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"
    PREPRODUCTION = "preproduction"
    STAGING = "staging"
    TEST = "test"


class LogLevel(StrEnum):
    """ENUM LogLevel."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class EnvironmentSettings(BaseSettings):
    """API Environment Settings."""

    ENVIRONMENT: Environment = Environment.PRODUCTION
    LOG_LEVEL: LogLevel = LogLevel.ERROR
    DEBUG: bool = False


class DatabaseSettings(BaseSettings):
    """Database Settings."""

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "@w3s0meP4ss"  # noqa: S105
    DB_DB: str = "syncit"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def DB_URI(self) -> PostgresDsn:  # noqa: N802
        """Validating DB_URI by building it with the DB environment variables."""
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_DB,
        )


class Settings(
    EnvironmentSettings,
    DatabaseSettings,
    BaseSettings,
):
    """API settings."""

    model_config = SettingsConfigDict(
        # .env.prod takes priority over `.env`
        env_file=(".env", ".env.prod"),
        extra="ignore",
    )

    @classmethod
    @lru_cache
    def get(cls) -> Self:
        """Get settings."""
        return cls()
