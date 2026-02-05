"""Metadata Mixin."""

from datetime import UTC, datetime

from sqlmodel import DateTime, Field, SQLModel, String


class MetadataMixin(SQLModel):
    """Mixins for metadata attributes."""

    created_at: datetime = Field(  # type: ignore[call-overload]
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        sa_type=DateTime(timezone=True),  # type: ignore[reportArgumentType]
        sa_column_args=[],
    )

    updated_at: datetime = Field(  # type: ignore[call-overload]
        default_factory=lambda: datetime.now(UTC),
        sa_type=DateTime(timezone=True),  # type: ignore[reportArgumentType]
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC)},
        nullable=False,
    )

    updated_by: str | None = Field(
        default=None,
        sa_type=String,
        nullable=True,
    )
