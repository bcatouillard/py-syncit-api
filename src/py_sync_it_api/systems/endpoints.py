"""Systems endpoint."""

from collections.abc import Sequence
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from .exceptions import SystemCreateError, SystemDeleteError, SystemNotFoundError, SystemReadError, SystemUpdateError
from .models import System
from .schemas import SystemCreateIn, SystemReadFilteredIn, SystemReadIn, SystemUpdateIn
from .services import SystemService

router = APIRouter(
    prefix="/systems",
    tags=["System"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    operation_id="create_system",
)
async def system_create(payload: SystemCreateIn, service: Annotated[SystemService, Depends(SystemService)]) -> System:
    """Create a new system entry."""
    try:
        return await service.create(payload)
    except SystemCreateError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e)) from e


@router.get("/{id}", operation_id="get_system")
async def system_read(id: UUID, service: Annotated[SystemService, Depends(SystemService)]) -> System:  # noqa: A002
    """Get a system entry by ID."""
    try:
        payload = SystemReadIn(id=id)
        return await service.read(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except SystemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except SystemReadError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("", operation_id="list_systems")
async def system_read_filtered_or_all(
    payload: Annotated[SystemReadFilteredIn, Query()],
    service: Annotated[SystemService, Depends(SystemService)],
) -> Sequence[System]:
    """Get all systems or filtered if payload provided."""
    try:
        return await service.read_filtered_or_all(payload)
    except SystemReadError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.patch("/{id}", operation_id="update_system")
async def cloudflare_billing_update(
    id: UUID,  # noqa: A002
    payload: SystemUpdateIn,
    service: Annotated[SystemService, Depends(SystemService)],
) -> System:
    """Update a billing entry."""
    try:
        return await service.update(id=id, payload=payload)
    except SystemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except SystemUpdateError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/{id}", operation_id="delete_system")
async def system_delete(id: UUID, service: Annotated[SystemService, Depends(SystemService)]) -> System:  # noqa: A002
    """Delete a billing entry."""
    try:
        return await service.delete(id)
    except SystemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except SystemDeleteError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
