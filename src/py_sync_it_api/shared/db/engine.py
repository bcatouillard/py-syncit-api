"""Postgresql DB engine."""

from typing import Annotated

from fastapi import Depends
from loguru import logger
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from py_sync_it_api.shared.dependencies import Settings
from py_sync_it_api.shared.utils.singleton import SingletonMeta


class AsyncDbEngine(metaclass=SingletonMeta):
    """AsyncDB Engine."""

    _engine: AsyncEngine
    _sessionfactory: async_sessionmaker[AsyncSession]

    def __init__(self, settings: Settings) -> None:
        """Represents Database.

        Args:
            settings (Settings): settings to be injected
        """
        self._engine = create_async_engine(
            url=settings.DB_URI.unicode_string(),  # type: ignore[attr-defined]
        )
        self._sessionfactory = async_sessionmaker(bind=self._engine, expire_on_commit=False)

    @staticmethod
    async def get_database_session(settings: Settings):  # noqa: ANN205
        """Create Database async session.

        Yields:
            AsyncSession: Database async session
        """
        async with AsyncDbEngine(settings)._sessionfactory() as session:  # pyright: ignore[reportAttributeAccessIssue] # noqa: SLF001
            try:
                yield session
            except Exception as e:
                logger.warning(f"Failed to create database session: {e}")
                raise
            finally:
                await session.close()


Db = Annotated[AsyncSession, Depends(AsyncDbEngine.get_database_session)]
