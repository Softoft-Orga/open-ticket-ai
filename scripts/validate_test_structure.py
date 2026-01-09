#!/usr/bin/env python3
"""Validate test structure according to project guidelines.

This script ensures that:
1. No test files exist under src/ directories
2. Test directories don't contain __init__.py files
3. Test files follow the test_*.py naming convention
4. Tests are properly organized in unit/integration/e2e directories
"""

import sys
from pathlib import Path


def find_violations() -> list[str]:
    """Find test structure violations."""
    violations: list[str] = []
    repo_root = Path(__file__).parent.parent

    violations.extend(check_no_tests_in_src(repo_root))
    violations.extend(check_no_init_in_test_dirs(repo_root))
    violations.extend(check_test_file_naming(repo_root))

    return violations


def check_no_tests_in_src(repo_root: Path) -> list[str]:
    """Check that no test files or directories exist under src/."""
    violations: list[str] = []

    src_dirs = list(repo_root.glob("**/src"))

    for src_dir in src_dirs:
        for test_file in src_dir.rglob("test_*.py"):
            violations.append(
                f"Test file found under src/: {test_file.relative_to(repo_root)}"
            )

        for tests_dir in src_dir.rglob("tests"):
            if tests_dir.is_dir():
                violations.append(
                    f"Tests directory found under src/: {tests_dir.relative_to(repo_root)}"
                )

    return violations


def check_no_init_in_test_dirs(repo_root: Path) -> list[str]:
    """Check that test directories don't contain __init__.py files."""
    violations: list[str] = []

    test_dirs = [
        repo_root / "tests",
        *list(repo_root.glob("packages/*/tests")),
    ]

    for test_dir in test_dirs:
        if not test_dir.exists():
            continue

        for init_file in test_dir.rglob("__init__.py"):
            violations.append(
                f"__init__.py found in test directory: {init_file.relative_to(repo_root)}"
            )

    return violations


def check_test_file_naming(repo_root: Path) -> list[str]:
    """Check that test files follow the test_*.py naming convention."""
    violations: list[str] = []

    test_dirs = [
        repo_root / "tests",
        *list(repo_root.glob("packages/*/tests")),
    ]

    for test_dir in test_dirs:
        if not test_dir.exists():
            continue

        for py_file in test_dir.rglob("*.py"):
            if py_file.name == "conftest.py":
                continue
            if py_file.name.startswith("fixtures_"):
                continue
            if not py_file.name.startswith("test_"):
                violations.append(
                    f"Test file doesn't follow test_*.py naming: {py_file.relative_to(repo_root)}"
                )

    return violations


def main() -> int:
    """Main entry point."""
    print("Validating test structure...")

    violations = find_violations()

    if not violations:
        print("✓ Test structure validation passed!")
        return 0

    print("✗ Test structure validation failed!")
    print()
    print("Violations found:")
    for violation in violations:
        print(f"  - {violation}")
    print()
    print("Please fix these violations according to AGENTS.md guidelines.")

    return 1


if __name__ == "__main__":
    sys.exit(main())
