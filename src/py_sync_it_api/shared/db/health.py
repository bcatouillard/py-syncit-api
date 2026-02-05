"""Database Healthcheck."""

from typing import Annotated
from venv import logger

from fastapi import Depends
from sqlalchemy import text
from sqlmodel import select

from .engine import Db


async def get_database_health(db: Db) -> bool:
    """Perform dummy db operation and return True if Db healthily responds.

    Args:
        db (Db): Database injected session

    Returns:
        bool: Is database healthy
    """
    try:
        async with db.begin():
            """Generated Query:
            SELECT "1";
            """
            result = await db.execute(select(text("1")))
            val = result.first()

            if val and val.tuple()[0] == 1:
                return True

        return False  # noqa: TRY300
    except Exception as e:  # noqa: BLE001
        logger.warning(
            f"Failed to ping DB, exceptions: {e}",
        )
        return False


DbHealth = Annotated[bool, Depends(get_database_health)]
