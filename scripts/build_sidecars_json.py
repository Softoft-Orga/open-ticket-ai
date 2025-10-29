#!/usr/bin/env python3
"""
Generate sidecars.json for runtime consumption by VitePress documentation.

This script scans the man_structured directory and creates a JSON file
containing all sidecar data organized by type and name.
"""

import json
import sys
from pathlib import Path
from typing import Any

import yaml


def to_snake_case(name: str) -> str:
    """Convert filename to snake_case identifier."""
    # Remove .sidecar.yml suffix
    if name.endswith(".sidecar.yml"):
        name = name[:-12]
    return name


def load_sidecar(filepath: Path) -> dict[str, Any] | None:
    """Load and parse a sidecar YAML file."""
    try:
        with open(filepath) as f:
            data: dict[str, Any] = yaml.safe_load(f)
            return data
    except OSError as e:
        print(f"Warning: Could not load {filepath}: {e}", file=sys.stderr)
        return None


def generate_sidecars_json(root_dir: Path, output_path: Path) -> int:
    """
    Generate sidecars.json from all sidecar files.

    Returns:
        0 on success, 1 on error
    """
    man_structured_dir = root_dir / "docs" / "_internal" / "man_structured"

    if not man_structured_dir.exists():
        print(f"Error: {man_structured_dir} does not exist", file=sys.stderr)
        return 1

    sidecars = []

    # Process each type directory
    for type_dir in ["pipes", "services", "triggers"]:
        type_path = man_structured_dir / type_dir

        if not type_path.exists():
            continue

        # Get singular form for type (pipe, service, trigger)
        sidecar_type = type_dir.rstrip("s")

        # Process each sidecar file
        for sidecar_file in sorted(type_path.glob("*.sidecar.yml")):
            data = load_sidecar(sidecar_file)

            if data is None:
                continue

            # Extract component name from filename
            name = to_snake_case(sidecar_file.name)

            # Create sidecar entry
            entry = {"name": name, "type": sidecar_type, "path": str(sidecar_file.relative_to(root_dir)), "data": data}

            sidecars.append(entry)

    # Write output file
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(sidecars, f, indent=2)

    print(f"✅ Generated {output_path}")
    print(f"   Added {len(sidecars)} sidecars:")

    # Count by type
    by_type: dict[str, int] = {}
    for entry in sidecars:
        # entry is dict[str, Any], extract type field
        entry_type = str(entry.get("type", "unknown"))
        by_type[entry_type] = by_type.get(entry_type, 0) + 1

    for sidecar_type, count in sorted(by_type.items()):
        print(f"     - {count} {sidecar_type}(s)")

    return 0


def main() -> int:
    """Main entry point."""
    root_dir = Path(__file__).parent.parent
    output_path = root_dir / "docs" / "public" / "assets" / "sidecars.json"

    print("🔨 Building sidecars.json...")
    print()

    result = generate_sidecars_json(root_dir, output_path)

    if result == 0:
        print()
        print("✅ Build complete!")
    else:
        print()
        print("❌ Build failed!")

    return result


if __name__ == "__main__":
    sys.exit(main())
