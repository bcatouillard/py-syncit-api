"""Systems schemas."""

from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, model_validator


class SystemTypeEnum(StrEnum):
    """System Type enum."""

    SALESFORCE = "Salesforce"
    ZENDESK = "ZENDESK"


class SystemCreateIn(BaseModel):
    """System input payload for creation.

    Attributes:
        name: The name of the system entity.
        type: The system type.
    """

    name: str
    type: SystemTypeEnum


class SystemReadIn(BaseModel):
    """System input payload for read operations.

    Attributes:
        id: The unique identifier of the system entity to retrieve.
    """

    id: UUID


class SystemReadFilteredIn(BaseModel):
    """System input payload for filtered read operations.

    Attributes:
        id: The unique identifier of the system entity to retrieve.
        name: The name of the system entity to retrieve.
        type: The system type.

    Note:
        Only one identifier should be provided. If both are provided, id takes precedence.
    """

    id: UUID | None = None
    name: str | None = None
    type: SystemTypeEnum | None = None


class SystemUpdateIn(BaseModel):
    """System input payload for update operations.

    Attributes:
        name: The name of the system entity.
        type: The system type.

    Raises:
        ValueError: Check if one field at least is provided.
    """

    name: str | None = None
    type: SystemTypeEnum | None = None

    @model_validator(mode="after")
    def check_at_least_one_field(self):  # noqa: ANN201
        """Ensure at least one field besides updated_by is provided for update."""
        if all(getattr(self, field) is None for field in ["name", "type"]):
            msg = "At least one identifier ['name', 'type'] is required."
            raise ValueError(msg)
        return self
