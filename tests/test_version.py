"""Test the dynamic version."""

import re

from py_sync_it_api import __version__


def test_version() -> None:
    """Test the version.

    We check that version is valid and is not the default one.
    """
    base_version = re.search(r"^\d+\.\d+\.\d+", __version__)
    assert base_version
    assert __version__ != "0.0.0.dev0+0"
