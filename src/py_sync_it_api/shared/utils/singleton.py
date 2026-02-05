"""Singleton implementation."""

from threading import Lock
from typing import Any


class SingletonMeta(type):
    """Add the Singleton behavior through a metaclass."""

    _instances: dict[type, Any] = {}  # noqa: RUF012
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs) -> dict[type, Any]:  # noqa: ANN002, ANN003
        """On call getting instantiated class."""
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance

        return cls._instances[cls]
