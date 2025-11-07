from __future__ import annotations

import argparse
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

from scripts.pdgen.generator import generate_plantuml  # noqa: E402
from scripts.pdgen.parser import parse_python_file, parse_python_files  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate PlantUML class diagrams from Python files with @include_in_uml decorator"
    )
    parser.add_argument(
        "path",
        type=Path,
        nargs="?",
        default=Path.cwd(),
        help="Path to the directory or file to analyze (default: current directory)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file path for the PlantUML diagram (default: stdout)",
    )

    args = parser.parse_args()

    path = args.path.resolve()
    if not path.exists():
        print(f"Error: Path '{path}' does not exist")
        return

    classes = parse_python_file(path) if path.is_file() else parse_python_files(path)

    diagram = generate_plantuml(classes)

    if args.output:
        args.output.write_text(diagram, encoding="utf-8")
        print(f"PlantUML diagram written to {args.output}")
    else:
        print(diagram)


if __name__ == "__main__":
    main()
