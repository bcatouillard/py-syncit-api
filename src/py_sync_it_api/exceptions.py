"""Exceptions module."""

from http import HTTPStatus

from fastapi import status
from pydantic import BaseModel, create_model


class _BaseError(BaseModel):
    """Base model for all exceptions raised by calling API methods.

    Complies with the APIM standard of error format.
    """

    error: str
    error_description: str


class ApiError(Exception):
    """Base class for all exceptions raised by calling API methods."""

    status_code: int = 500
    description: str = "Internal server error"
    model: type[_BaseError] = create_model(
        "ApiError",
        __base__=_BaseError,
        __doc__="Base class for all exceptions raised by calling API methods.",
    )

    def __init__(self, description: str | None = None) -> None:
        """Instantiate the base custom HTTP error."""
        if description:
            self.description = description
        if not self.description:
            self.description = HTTPStatus(self.status_code).phrase

    @classmethod
    def response(cls) -> dict[int, dict[str, type[_BaseError]]]:
        """Returns the response model for the exception."""
        return {cls.status_code: {"model": cls.model}}


class UnprocessableEntityError(ApiError):
    """Exception raised when the request validation fails."""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    model: type[_BaseError] = create_model("UnprocessableEntityError", __base__=_BaseError)


class ConflictError(ApiError):
    """Exception raised when the request causes conflict."""

    status_code = status.HTTP_409_CONFLICT
    model: type[_BaseError] = create_model("ConflictError", __base__=_BaseError)


class BadRequestError(ApiError):
    """Exception raised when the request is not valid."""

    status_code = status.HTTP_400_BAD_REQUEST
    model: type[_BaseError] = create_model("BadRequestError", __base__=_BaseError)
