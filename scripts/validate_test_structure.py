#!/usr/bin/env python3
"""Validate test structure according to AGENTS.md guidelines.

This script enforces the following rules:
1. No test files under src/ paths (src/**/tests, src/**/test_*.py)
2. Test files must follow test_*.py naming convention
3. No __init__.py files in test directories
4. Tests should be in tests/ or packages/*/tests/ directories
"""

from pathlib import Path
import sys


def find_forbidden_test_files(repo_root: Path) -> list[Path]:
    """Find test files under src/ that violate the rules."""
    forbidden = []
    
    # Find all test directories under src/
    src_dir = repo_root / "src"
    if src_dir.exists():
        # Check for test directories under src/
        for test_dir in src_dir.rglob("tests"):
            if test_dir.is_dir():
                forbidden.append(test_dir)
        
        # Check for test_*.py files under src/
        for test_file in src_dir.rglob("test_*.py"):
            forbidden.append(test_file)
    
    return forbidden


def find_test_init_files(repo_root: Path) -> list[Path]:
    """Find __init__.py files in test directories."""
    init_files = []
    
    # Check root tests/
    tests_dir = repo_root / "tests"
    if tests_dir.exists():
        for init_file in tests_dir.rglob("__init__.py"):
            init_files.append(init_file)
    
    # Check packages/*/tests/
    packages_dir = repo_root / "packages"
    if packages_dir.exists():
        for package in packages_dir.iterdir():
            if package.is_dir():
                package_tests = package / "tests"
                if package_tests.exists():
                    for init_file in package_tests.rglob("__init__.py"):
                        init_files.append(init_file)
    
    return init_files


def find_incorrectly_named_tests(repo_root: Path) -> list[Path]:
    """Find test files that don't follow test_*.py naming convention."""
    incorrect = []
    
    # Allowed patterns: test_*.py, conftest.py, fixtures_*.py, and helper modules
    # Helper modules are allowed: factories.py, mocked_*.py, etc. in test directories
    # E2E demo scripts like main.py are also allowed
    allowed_names = {"conftest.py", "__init__.py", "main.py"}
    allowed_prefixes = ("test_", "fixtures_")
    allowed_patterns = ("factories.py", "mocked_", "helpers.py")
    
    def is_allowed(filename: str) -> bool:
        """Check if a filename is allowed in test directories."""
        if filename in allowed_names:
            return True
        if any(filename.startswith(prefix) for prefix in allowed_prefixes):
            return True
        if any(pattern in filename for pattern in allowed_patterns):
            return True
        return False
    
    # Check root tests/
    tests_dir = repo_root / "tests"
    if tests_dir.exists():
        for py_file in tests_dir.rglob("*.py"):
            if not is_allowed(py_file.name):
                incorrect.append(py_file)
    
    # Check packages/*/tests/
    packages_dir = repo_root / "packages"
    if packages_dir.exists():
        for package in packages_dir.iterdir():
            if package.is_dir():
                package_tests = package / "tests"
                if package_tests.exists():
                    for py_file in package_tests.rglob("*.py"):
                        if not is_allowed(py_file.name):
                            incorrect.append(py_file)
    
    return incorrect


def main() -> int:
    """Run all validation checks."""
    repo_root = Path(__file__).parent.parent
    errors = []
    
    print("🔍 Validating test structure according to AGENTS.md...")
    print(f"Repository root: {repo_root}")
    print()
    
    # Check for forbidden test files under src/
    forbidden = find_forbidden_test_files(repo_root)
    if forbidden:
        errors.append("❌ CRITICAL: Test files found under src/ (forbidden by AGENTS.md)")
        errors.append("   Rule: Never place tests under any src/ path")
        errors.append("   Forbidden patterns: src/**/tests, src/**/test_*.py")
        for path in forbidden:
            errors.append(f"   - {path.relative_to(repo_root)}")
        errors.append("")
    
    # Check for __init__.py in test directories
    init_files = find_test_init_files(repo_root)
    if init_files:
        errors.append("❌ __init__.py files found in test directories")
        errors.append("   Rule: NO __init__.py files in test directories")
        errors.append("   Test directories are not Python packages")
        for path in init_files:
            errors.append(f"   - {path.relative_to(repo_root)}")
        errors.append("")
    
    # Check for incorrectly named test files
    incorrect = find_incorrectly_named_tests(repo_root)
    if incorrect:
        errors.append("⚠️  Test files not following naming convention")
        errors.append("   Rule: Test files must be test_*.py")
        errors.append("   Allowed: test_*.py, conftest.py, fixtures_*.py")
        for path in incorrect:
            errors.append(f"   - {path.relative_to(repo_root)}")
        errors.append("")
    
    # Report results
    if errors:
        print("❌ Test structure validation FAILED")
        print()
        for error in errors:
            print(error)
        print()
        print("Please fix the issues above to comply with AGENTS.md guidelines.")
        print("See AGENTS.md for the authoritative test structure rules.")
        return 1
    else:
        print("✅ All test structure validations passed!")
        print()
        print("Validated:")
        print("  ✓ No test files under src/")
        print("  ✓ No __init__.py in test directories")
        print("  ✓ Test files follow naming conventions")
        return 0


if __name__ == "__main__":
    sys.exit(main())
