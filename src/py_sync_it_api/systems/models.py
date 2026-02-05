"""SQL Model for Billing."""

from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

from py_sync_it_api.shared.models.mixins import MetadataMixin

from .schemas import SystemTypeEnum


class SystemBase(MetadataMixin, SQLModel):
    """System base model."""

    id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True)
    name: str = Field(index=True)
    type: SystemTypeEnum = Field()


class System(SystemBase, table=True):
    """SQLModel who represents System object and table."""
