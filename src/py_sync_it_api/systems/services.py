"""Services for Cloudflare Billing."""

from collections.abc import Sequence
from uuid import UUID

from loguru import logger
from sqlalchemy import or_, select
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from py_sync_it_api.shared.db.engine import Db

from .exceptions import SystemCreateError, SystemDeleteError, SystemNotFoundError, SystemReadError, SystemUpdateError
from .models import System
from .schemas import SystemCreateIn, SystemReadFilteredIn, SystemReadIn, SystemUpdateIn


class SystemService:
    """System class."""

    def __init__(self, db: Db) -> None:
        """Initiate System class.

        Args:
            db (Db): database connection
        """
        self.db = db

    async def read(self, payload: SystemReadIn) -> System:
        """Read System entry.

        Args:
            payload (SystemReadIn): system entry input (contains id)

        Raises:
            SystemNotFoundError: Dedicated error for the get.

        Returns:
            System: System entry from database.
        """
        try:
            logger.debug("start read system input", payload=payload)
            query = select(System).where(System.id == payload.id)  # pyright: ignore[reportArgumentType]
            response = await self.db.execute(query)
            result = response.scalars().one_or_none()
            if not result:
                message = f"System id '{payload.id}' not found"
                logger.warning(message, payload=payload)
                raise SystemNotFoundError(message)
            else:  # noqa: RET506
                return result
        except SQLAlchemyError as e:
            message = "Failed to read System entry."
            logger.error(message, payload=payload, exception=e)
            raise SystemReadError(message) from e

    async def read_filtered_or_all(self, payload: SystemReadFilteredIn) -> Sequence[System]:
        """Retrieve System records based on filter criteria or none.

        Args:
            payload: The filter criteria (cex, name, business_unit)

        Returns:
            Sequence[System]: List of System items matching the criteria

        Raises:
            CloudflareSystemReadError: Dedicated error for the get.
        """
        query = select(System)
        filters = []
        if payload.name is not None:
            filters.append(System.name.ilike(f"%{payload.name}%"))  # pyright: ignore[reportAttributeAccessIssue]
        if payload.type is not None:
            filters.append(System.type.ilike(f"%{payload.type}%"))  # pyright: ignore[reportAttributeAccessIssue]
        if filters:
            query = query.where(or_(*filters))

        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, payload: SystemCreateIn) -> System:
        """Read System entry.

        Args:
            payload (SystemCreateIn): inputs of System item.

        Raises:
            SystemReadError: Dedicated error for the creation.

        Returns:
            System: System entry from database.
        """
        try:
            logger.debug("start create System input", payload=payload)
            system_sql = System(
                name=payload.name,
                type=payload.type,
            )
            self.db.add(system_sql)
            await self.db.commit()
            await self.db.refresh(system_sql)
            return system_sql  # noqa: TRY300
        except SQLAlchemyError as e:
            message = "Failed to create System entry."
            logger.error(message, payload=payload, exception=e)
            raise SystemCreateError(message) from e

    async def update(
        self,
        id: UUID,  # noqa: A002
        payload: SystemUpdateIn,
    ) -> System:
        """Update System entry.

        Args:
            id (UUID): resource id.
            payload (SystemUpdateIn): inputs of System item.

        Raises:
            CloudflareSystemCreateError: Dedicated error for the update.

        Returns:
            System: System entry from database.
        """
        logger.debug("start update System input", payload=payload)
        query = select(System).where(System.id == id)  # pyright: ignore[reportArgumentType]
        result = await self.db.execute(query)
        try:
            system_object = result.scalars().one()
        except NoResultFound as e:
            message = f"System id '{id}' not found"
            logger.error(message, payload=payload)
            raise SystemNotFoundError(message) from e

        for key, value in payload.model_dump(exclude_none=True, exclude_unset=True).items():
            if hasattr(system_object, key):
                setattr(system_object, key, value)

        try:
            await self.db.commit()
            await self.db.refresh(system_object)
            return system_object  # noqa: TRY300
        except Exception as e:
            await self.db.rollback()
            message = "Failed to update System entry."
            logger.error(message, payload=payload, exception=e)
            raise SystemUpdateError(message) from e

    async def delete(self, system_id: UUID) -> System:
        """Delete System entry.

        Args:
            system_id (UUID): The System data containing the ID to delete

        Returns:
            SystemDeleteOut: System id and name deleted.

        Raises:
            SystemDeleteError: Dedicated error for the update.
        """
        query = (
            select(System).where(System.id == system_id)  # pyright: ignore[reportArgumentType]
        )
        result = await self.db.execute(query)
        system_object = result.scalars().one_or_none()

        if not system_object:
            message = f"System with id '{system_id}' not found."
            logger.error(message, system_id=system_id)
            raise SystemNotFoundError(message)

        try:
            await self.db.delete(system_object)
            await self.db.commit()
            return system_object  # noqa: TRY300
        except Exception as e:
            await self.db.rollback()
            message = "Failed to delete System entry."
            logger.error(message, System_id=system_id, exception=e)
            raise SystemDeleteError(message) from e
