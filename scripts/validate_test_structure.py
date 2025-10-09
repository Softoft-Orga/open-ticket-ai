#!/usr/bin/env python3
"""Validate test structure compliance with AGENTS.md."""

from __future__ import annotations

import sys
from pathlib import Path


def find_violations() -> list[str]:
    violations: list[str] = []
    repo_root = Path(__file__).parent.parent

    src_dir = repo_root / "src"
    if src_dir.exists():
        for path in src_dir.rglob("*"):
            if path.is_file() and (
                path.name.startswith("test_") or path.name.endswith("_test.py")
            ):
                rel_path = path.relative_to(repo_root)
                violations.append(f"Test file found under src/: {rel_path}")

            if path.is_dir() and path.name == "tests":
                rel_path = path.relative_to(repo_root)
                violations.append(f"Test directory found under src/: {rel_path}")

    for test_location in [repo_root / "tests", repo_root / "packages"]:
        if not test_location.exists():
            continue

        for tests_dir in test_location.rglob("tests"):
            if tests_dir.is_dir() and ".venv" not in str(tests_dir):
                init_file = tests_dir / "__init__.py"
                if init_file.exists():
                    rel_path = init_file.relative_to(repo_root)
                    violations.append(
                        f"Test directory should not contain __init__.py: {rel_path}"
                    )

    return violations


def main() -> int:
    violations = find_violations()

    if violations:
        print("❌ Test structure violations found:\n", file=sys.stderr)
        for violation in violations:
            print(f"  - {violation}", file=sys.stderr)
        print(
            "\nSee AGENTS.md for test structure requirements.",
            file=sys.stderr,
        )
        return 1

    print("✅ Test structure validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
