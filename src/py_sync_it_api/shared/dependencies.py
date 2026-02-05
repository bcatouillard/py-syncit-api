"""Global dependencies."""

from typing import Annotated

from fastapi import Depends

from .settings import Settings as _Settings

Settings = Annotated[_Settings, Depends(_Settings.get)]
