"""Sync It module."""

from importlib.metadata import version

from .app import app

__version__ = version("py_sync_it_api")  # pragma: no cover

__all__ = [
    "__version__",
    "app",
]
