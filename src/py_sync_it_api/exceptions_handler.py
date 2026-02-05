"""Exceptions handler module."""

from http import HTTPStatus

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .exceptions import ApiError


async def fallback_exception_handler(_r: Request, _e: Exception) -> JSONResponse:
    """Permits to catch all Exception in last resort to avoid to leak data to clients.

    It also permit to answer client JSONResponse in any case.

    Args:
        req (Request): The request being processed
        e (Exception): Exception caught

    Returns:
        JSONResponse: Response send to client.
    """
    _e, _r = _e, _r  # Trick to pick the reference to self object  # noqa: PLW0127
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ApiError.model(
            error="Internal server error.",
            # Do not embbed e as we do not master the exception we don't want to leak information
            error_description="An unhandled error occurred. Please contact support if the issue persists.",
        ).model_dump(),
    )


async def http_exception_handler(_: Request, e: HTTPException) -> JSONResponse:
    """Handles HTTP exceptions to comply with the API Decathlon design standard.

    Returns:
        JSONResponse: The JSON response to send to the client.
    """
    return JSONResponse(
        status_code=e.status_code,
        content=ApiError.model(
            error=HTTPStatus(e.status_code).phrase,
            error_description=str(e.detail),
        ).model_dump(),
    )


async def validation_exception_handler(_: Request, e: RequestValidationError) -> JSONResponse:
    """Handles validation exceptions to comply with the API Decathlon design standard."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ApiError.model(
            error=HTTPStatus(status.HTTP_422_UNPROCESSABLE_ENTITY).phrase,
            error_description=str(e),
        ).model_dump(),
    )


async def custom_http_exception_handler(_: Request, e: ApiError) -> JSONResponse:
    """Handles custom http exception to comply with the API Decathlon design standard."""
    return JSONResponse(
        status_code=e.status_code,
        content=ApiError.model(
            error=HTTPStatus(e.status_code).phrase,
            error_description=e.description,
        ).model_dump(),
    )
