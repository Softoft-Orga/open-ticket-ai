"""Remove comment tokens from git-tracked Python files.

This utility is intended to be run in automated contexts (for example GitHub
Actions) to ensure the code base does not contain ``#`` style Python comments.
It preserves file encodings, docstrings, shebang lines, and encoding
annotations while stripping standalone and inline comments.
"""

from __future__ import annotations

import argparse
import io
import subprocess
import tokenize
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileChange:
    """Representation of a Python file rewritten by the tool."""

    path: Path
    updated_source: str
    encoding: str

    def apply(self) -> None:
        self.path.write_text(self.updated_source, encoding=self.encoding)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List files that would be changed without rewriting them.",
    )
    return parser.parse_args(argv)


def list_tracked_python_files(root: Path) -> Iterable[Path]:
    result = subprocess.run(
        ["git", "ls-files", "*.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    for line in result.stdout.splitlines():
        if line.strip():
            yield root / line.strip()


def should_preserve_comment(token: tokenize.TokenInfo) -> bool:
    text = token.string
    line_no = token.start[0]

    if line_no == 1 and text.startswith("#!"):
        return True

    if line_no in (1, 2) and "coding" in text.lower():
        return True

    return False


def strip_comments(source_bytes: bytes) -> tuple[str, str]:
    """Return the rewritten source and detected encoding."""

    stream = io.BytesIO(source_bytes)
    encoding, _ = tokenize.detect_encoding(stream.readline)
    stream.seek(0)

    tokens = tokenize.tokenize(stream.readline)
    filtered_tokens: list[tokenize.TokenInfo] = []

    for token in tokens:
        if token.type == tokenize.COMMENT and not should_preserve_comment(token):
            continue
        filtered_tokens.append(token)

    rebuilt = tokenize.untokenize(filtered_tokens)
    if isinstance(rebuilt, bytes):
        rebuilt_text = rebuilt.decode(encoding)
    else:
        rebuilt_text = rebuilt
    return rebuilt_text, encoding


def ensure_trailing_newline(text: str) -> str:
    return text if text.endswith("\n") else text + "\n"


def collect_changes(files: Iterable[Path]) -> list[FileChange]:
    changes: list[FileChange] = []
    for path in files:
        original_bytes = path.read_bytes()
        rewritten, encoding = strip_comments(original_bytes)
        original_text = original_bytes.decode(encoding)

        normalized_original = ensure_trailing_newline(original_text)
        normalized_rewritten = ensure_trailing_newline(rewritten)

        if normalized_rewritten != normalized_original:
            changes.append(
                FileChange(
                    path=path,
                    updated_source=normalized_rewritten,
                    encoding=encoding,
                )
            )
    return changes


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()

    python_files = list(list_tracked_python_files(root))
    if not python_files:
        print("No Python files detected.")
        return 0

    changes = collect_changes(python_files)
    if not changes:
        print("No comments found to remove.")
        return 0

    if args.dry_run:
        print("Files that would be rewritten:")
        for change in changes:
            print(f" - {change.path.relative_to(root)}")
        return 0

    for change in changes:
        change.apply()
        print(f"Rewrote {change.path.relative_to(root)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
