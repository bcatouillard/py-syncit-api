"""Exceptions for System."""

from fastapi import status


class SystemBaseError(Exception):
    """Base exception for System errors."""


class SystemCreateError(SystemBaseError):
    """Error dedicated to the System Read endpoint.

    Args:
        text: The error message.
        severity: The severity of the error ['error', 'warning']. Defaults to 'error'.
        status_code: The status code of the error. Defaults to 500.
    """

    def __init__(
        self,
        text: str,
        severity: str = "error",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:
        """Init a FastAPI with a mandatory text."""
        super().__init__(text)
        self.message = text
        self.severity = severity
        self.status_code = status_code


class SystemReadError(SystemBaseError):
    """Error dedicated to the System Read endpoint.

    Args:
        text: The error message.
        severity: The severity of the error ['error', 'warning']. Defaults to 'error'.
        status_code: The status code of the error. Defaults to 500.
    """

    def __init__(
        self,
        text: str,
        severity: str = "error",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:
        """Init a FastAPI Error with a mandatory text."""
        super().__init__(text)
        self.message = text
        self.severity = severity
        self.status_code = status_code


class SystemNotFoundError(SystemReadError):
    """Exception raised when a system entry is not found."""


class SystemUpdateError(SystemBaseError):
    """Error dedicated to the System Read endpoint.

    Args:
        text: The error message.
        severity: The severity of the error ['error', 'warning']. Defaults to 'error'.
        status_code: The status code of the error. Defaults to 500.
    """

    def __init__(
        self,
        text: str,
        severity: str = "error",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:
        """Init a FastAPI with a mandatory text."""
        super().__init__(text)
        self.message = text
        self.severity = severity
        self.status_code = status_code


class SystemDeleteError(SystemBaseError):
    """Error dedicated to the System Delete endpoint.

    Args:
        text: The error message.
        severity: The severity of the error ['error', 'warning']. Defaults to 'error'.
        status_code: The status code of the error. Defaults to 500.
    """

    def __init__(
        self,
        text: str,
        severity: str = "error",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:
        """Init a FastAPI with a mandatory text."""
        super().__init__(text)
        self.message = text
        self.severity = severity
        self.status_code = status_code
