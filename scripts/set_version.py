#!/usr/bin/env python3
"""Set version across all packages in the workspace."""

import sys
from pathlib import Path


def set_version(version: str) -> None:
    """Set the same version in all pyproject.toml files."""
    import tomllib
    
    root = Path(__file__).parent.parent
    toml_files = [
        root / "pyproject.toml",
        root / "packages" / "otai_hf_local" / "pyproject.toml",
        root / "packages" / "otai_otobo_znuny" / "pyproject.toml",
    ]
    
    for toml_file in toml_files:
        if not toml_file.exists():
            print(f"Warning: {toml_file} not found")
            continue
            
        content = toml_file.read_text()
        
        with toml_file.open("rb") as f:
            data = tomllib.load(f)
        
        old_version = data["project"]["version"]
        
        new_content = content.replace(
            f'version = "{old_version}"',
            f'version = "{version}"'
        )
        
        toml_file.write_text(new_content)
        print(f"✓ {toml_file.relative_to(root)}: {old_version} → {version}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: set_version.py <version>")
        print("Example: set_version.py 1.0.18")
        sys.exit(1)
    
    version = sys.argv[1]
    
    if not version[0].isdigit():
        print(f"Error: Version must start with a digit, got: {version}")
        sys.exit(1)
    
    set_version(version)
    print(f"\n✓ All packages updated to version {version}")


if __name__ == "__main__":
    main()
