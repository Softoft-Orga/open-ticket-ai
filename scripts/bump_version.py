# scripts/bump_version.py
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Literal

import semver
import typer

App = typer.Typer(add_completion=False)



def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


def latest_tag() -> str | None:
    tags = run(["git", "tag", "--list", "v[0-9]*.[0-9]*.[0-9]*", "--sort=-v:refname"]).splitlines()
    return tags[0] if tags else None


def ensure_repo_root() -> None:
    repo = run(["git", "rev-parse", "--show-toplevel"])
    if Path.cwd().resolve() != Path(repo).resolve():
        raise RuntimeError("Run in repo root")


def ensure_clean(allow_dirty: bool) -> None:
    dirty = bool(run(["git", "status", "--porcelain"]))
    if dirty and not allow_dirty:
        raise RuntimeError("Working tree is dirty")


def bump(ver: str, kind: Literal["major", "minor", "patch"]) -> str:
    v = semver.Version.parse(ver.lstrip("v"))
    match kind:
        case "major":
            v = v.bump_major()
        case "minor":
            v = v.bump_minor()
        case "patch":
            v = v.bump_patch()
    return f"v{v}"


@App.command()
def main(
        kind: Literal["major", "minor", "patch"] = "patch",
        push: bool = False,
        allow_dirty: bool = False,
        start: str = "v0.1.0",
) -> None:
    ensure_repo_root()
    ensure_clean(allow_dirty)
    current = latest_tag() or start
    new = bump(current, kind)
    run(["git", "tag", "-a", new, "-m", new])
    if new not in run(["git", "tag", "--list"]).splitlines():
        raise RuntimeError(f"Tag {new} was not created")
    if push:
        run(["git", "push", "origin", new])
    print(new)


if __name__ == "__main__":
    App()
