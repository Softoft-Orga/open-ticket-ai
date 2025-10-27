from __future__ import annotations

from pathlib import Path

from setuptools_scm import get_version


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    version = get_version(
        root=root,
        version_scheme="only-version",
        local_scheme="no-local-version",
        tag_regex=r"^v(?P<version>\d+\.\d+\.\d+)$",
    )
    print(version)


if __name__ == "__main__":
    main()
