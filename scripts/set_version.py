#!/usr/bin/env python3
"""Set version across all packages in the workspace using uv."""

import subprocess
import sys


def set_version(version: str) -> None:
    """Set the same version in all packages using uv version command."""
    packages = [
        ("Core", None),
        ("HF Local", "otai_hf_local"),
        ("OTOBO/Znuny", "otai_otobo_znuny"),
    ]

    for name, package in packages:
        cmd = ["uv", "version", version]
        if package:
            cmd.extend(["--package", package])

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"✗ Failed to set {name} version: {result.stderr}")
            sys.exit(1)

        print(f"✓ {name:20} → {version}")


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
