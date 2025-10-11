#!/usr/bin/env python3
"""
Validate test structure compliance with AGENTS.md rules.

This script ensures that:
1. No test files exist under src/
2. All test directories follow the required structure
3. No __init__.py files exist in test directories
4. Test files follow naming conventions (test_*.py)
"""

import sys
from pathlib import Path


def find_violations() -> list[str]:
    """Find all test structure violations in the repository."""
    violations: list[str] = []
    repo_root = Path(__file__).parent.parent

    # Check for test files under src/
    src_dir = repo_root / "src"
    if src_dir.exists():
        violations.extend(
            f"❌ Test file found under src/: {test_file.relative_to(repo_root)}"
            for test_file in src_dir.rglob("test_*.py")
        )
        violations.extend(
            f"❌ Test file found under src/: {test_file.relative_to(repo_root)}"
            for test_file in src_dir.rglob("*_test.py")
        )
        violations.extend(
            f"❌ Test directory found under src/: {test_dir.relative_to(repo_root)}"
            for test_dir in src_dir.rglob("tests")
            if test_dir.is_dir()
        )

    # Check for __init__.py in test directories
    tests_dir = repo_root / "tests"
    if tests_dir.exists():
        violations.extend(
            f"❌ __init__.py found in test directory: {init_file.relative_to(repo_root)}"
            for init_file in tests_dir.rglob("__init__.py")
        )

    packages_dir = repo_root / "packages"
    if packages_dir.exists():
        for package in packages_dir.iterdir():
            if not package.is_dir():
                continue
            package_tests = package / "tests"
            if package_tests.exists():
                violations.extend(
                    f"❌ __init__.py found in test directory: {init_file.relative_to(repo_root)}"
                    for init_file in package_tests.rglob("__init__.py")
                )

    # Check for incorrectly named test files (*_test.py instead of test_*.py)
    if tests_dir.exists():
        violations.extend(
            f"❌ Incorrect test file naming (should be test_*.py): {test_file.relative_to(repo_root)}"
            for test_file in tests_dir.rglob("*_test.py")
        )

    if packages_dir.exists():
        for package in packages_dir.iterdir():
            if not package.is_dir():
                continue
            package_tests = package / "tests"
            if package_tests.exists():
                violations.extend(
                    f"❌ Incorrect test file naming (should be test_*.py): {test_file.relative_to(repo_root)}"
                    for test_file in package_tests.rglob("*_test.py")
                )

    return violations


def main() -> int:
    """Run validation and return exit code."""
    print("🔍 Validating test structure compliance with AGENTS.md rules...\n")

    violations = find_violations()

    if violations:
        print("❌ Test structure violations found:\n")
        for violation in violations:
            print(f"  {violation}")
        print(
            f"\n❌ Found {len(violations)} violation(s). Please fix them to comply with AGENTS.md rules."
        )
        print("\nRules:")
        print("  1. Never place tests under src/")
        print("  2. No __init__.py files in test directories")
        print("  3. Test files must be named test_*.py (not *_test.py)")
        print("  4. Unit tests go in packages/<name>/tests/ or tests/unit/")
        print("  5. Integration/e2e tests go in tests/integration/ or tests/e2e/")
        return 1
    else:
        print("✅ All test structure rules are satisfied!")
        print("\nValidated:")
        print("  ✓ No test files under src/")
        print("  ✓ No __init__.py files in test directories")
        print("  ✓ All test files follow test_*.py naming convention")
        return 0


if __name__ == "__main__":
    sys.exit(main())
