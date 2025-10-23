from __future__ import annotations

from importlib import metadata as importlib_metadata
from pathlib import Path

try:
    __version__ = importlib_metadata.version("open_ticket_ai")
except importlib_metadata.PackageNotFoundError:
    from setuptools_scm import get_version

    __version__ = get_version(
        root=Path(__file__).resolve().parents[1],
        version_scheme="guess-next-dev",
        local_scheme="no-local-version",
    )

__all__ = ["__version__"]
