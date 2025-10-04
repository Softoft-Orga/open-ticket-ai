"""Generate VitePress Markdown documentation for pipeline pipes from sidecar files.

This module reads pipe "sidecar" YAML files that describe the behaviour of
individual pipes and pairs them with the actual Python implementation. The
combined information is rendered as Markdown pages that can be dropped into the
VitePress documentation tree.

Key features
------------
* Discovers sidecar definitions recursively within a directory.
* Resolves dotted Python class paths to their source files, falling back to an
  AST search when the module path no longer matches the implementation.
* Supports multi-language sidecar metadata with graceful fallbacks.
* Produces frontmatter-aware Markdown including configuration tables, output
  schemas, error handling, examples, and implementation snippets.

The module exposes a reusable :func:`generate_pipe_docs` function and a Typer
CLI entry point so it can be invoked as ``python -m`` or wired into existing
build tooling.
"""

from __future__ import annotations

import ast
import importlib
import inspect
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

import typer
import yaml


@dataclass
class CodeReference:
    """Holds metadata about a resolved Python class implementation."""

    class_name: str
    module_path: str | None
    file_path: Path | None
    class_docstring: str | None
    source: str | None


def _slugify(value: str) -> str:
    """Return a filesystem friendly slug."""

    import re

    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "pipe"


def _ensure_absolute(path: Path) -> Path:
    return path if path.is_absolute() else path.resolve()


def _resolve_code_reference(class_path: str, source_root: Path) -> CodeReference:
    """Resolve ``class_path`` to implementation metadata."""

    module_name, _, class_name = class_path.rpartition(".")
    source_root = _ensure_absolute(source_root)

    if module_name:
        try:
            module = importlib.import_module(module_name)
            cls = getattr(module, class_name)
            source = inspect.getsource(cls)
            source_file = inspect.getsourcefile(cls)
            return CodeReference(
                class_name=class_name,
                module_path=module_name,
                file_path=Path(source_file).resolve() if source_file else None,
                class_docstring=inspect.getdoc(cls),
                source=source,
            )
        except (ModuleNotFoundError, AttributeError, OSError, TypeError):
            pass

    matches: list[tuple[Path, ast.ClassDef, ast.Module, str]] = []
    for py_path in source_root.rglob("*.py"):
        try:
            content = py_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        try:
            tree = ast.parse(content)
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                matches.append((py_path, node, tree, content))

    chosen: tuple[Path, ast.ClassDef, ast.Module, str] | None = None
    if matches:
        guessed_module_path = Path(*module_name.split(".")) if module_name else None
        guessed_file: Path | None = None
        if guessed_module_path:
            guessed_py = (source_root / guessed_module_path).with_suffix(".py")
            if guessed_py.is_file():
                guessed_file = guessed_py.resolve()
            else:
                guessed_dir = source_root / guessed_module_path
                init_file = guessed_dir / "__init__.py"
                if init_file.is_file():
                    guessed_file = init_file.resolve()
        if guessed_file:
            for candidate in matches:
                if candidate[0].resolve() == guessed_file:
                    chosen = candidate
                    break
        if not chosen:
            chosen = matches[0]

    if chosen:
        py_path, node, tree, content = chosen
        lines = content.splitlines()
        start = node.lineno - 1
        end = getattr(node, "end_lineno", None)
        if end is None:
            end = node.body[-1].lineno if node.body else node.lineno
        snippet = "\n".join(lines[start:end])
        class_docstring = ast.get_docstring(node)
        try:
            relative = py_path.resolve().relative_to(source_root)
            if py_path.name == "__init__.py":
                relative = relative.parent
            actual_module = ".".join(relative.with_suffix("").parts)
        except ValueError:
            actual_module = module_name or None
        return CodeReference(
            class_name=class_name,
            module_path=actual_module or module_name or None,
            file_path=py_path.resolve(),
            class_docstring=class_docstring,
            source=snippet,
        )

    return CodeReference(
        class_name=class_name,
        module_path=module_name or None,
        file_path=None,
        class_docstring=None,
        source=None,
    )


def _localise(value: Any, language: str) -> str | None:
    """Return the value translated into ``language`` if possible."""

    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        if language in value and value[language] not in (None, ""):
            return str(value[language])
        for candidate in value.values():
            if candidate:
                return str(candidate)
    return str(value)


def _normalise_summary(summary: str | None) -> str | None:
    if not summary:
        return None
    return " ".join(summary.strip().split())


def _format_yaml_block(data: Any) -> str:
    return yaml.safe_dump(data, sort_keys=False).strip()


def _relative_path(path: Path | None, base: Path) -> str | None:
    if path is None:
        return None
    try:
        return str(path.resolve().relative_to(base.resolve()))
    except ValueError:
        return str(path.resolve())


def _add_section(lines: list[str], title: str) -> None:
    lines.append(f"## {title}")
    lines.append("")


def _build_markdown(
    data: dict[str, Any],
    code_ref: CodeReference,
    language: str,
    project_root: Path,
    sidecar_path: Path,
) -> str:
    title = _localise(data.get("_title"), language) or code_ref.class_name
    summary = _normalise_summary(_localise(data.get("_summary"), language))

    frontmatter = {"title": title}
    if summary:
        frontmatter["description"] = summary

    lines: list[str] = ["---", yaml.safe_dump(frontmatter, sort_keys=False).strip(), "---", ""]
    lines.append("<!-- Generated by python_extras.scripts.doc_generation.generate_pipe_docs -->")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")

    metadata: list[str] = []
    class_path = data.get("_class")
    if class_path:
        metadata.append(f"- **Python class:** `{class_path}`")
    if data.get("_extends"):
        metadata.append(f"- **Extends:** `{data['_extends']}`")
    if data.get("_category"):
        metadata.append(f"- **Category:** `{data['_category']}`")
    if code_ref.module_path:
        metadata.append(f"- **Module:** `{code_ref.module_path}`")
    source_rel = _relative_path(code_ref.file_path, project_root)
    if source_rel:
        metadata.append(f"- **Source:** `{source_rel}`")
    sidecar_rel = _relative_path(sidecar_path, project_root)
    metadata.append(f"- **Sidecar:** `{sidecar_rel}`")

    if metadata:
        lines.extend(metadata)
        lines.append("")

    if summary:
        _add_section(lines, "Summary")
        lines.append(summary)
        lines.append("")

    if code_ref.class_docstring or code_ref.source:
        _add_section(lines, "Implementation")
        if code_ref.class_docstring:
            lines.append(textwrap.dedent(code_ref.class_docstring).strip())
            lines.append("")
        if code_ref.source:
            lines.append("```python")
            lines.append(textwrap.dedent(code_ref.source).strip())
            lines.append("```")
            lines.append("")

    inputs = data.get("_inputs", {})
    defaults = data.get("_defaults", {}) or {}
    config_model = inputs.get("config") if isinstance(inputs, dict) else None
    params = inputs.get("params") if isinstance(inputs, dict) else None
    if config_model or params:
        _add_section(lines, "Configuration")
        if config_model:
            lines.append(f"**Config model:** `{config_model}`")
            lines.append("")
        if isinstance(params, dict) and params:
            lines.append("### Parameters")
            lines.append("")
            lines.append("| Name | Description |")
            lines.append("| --- | --- |")
            for name, description in params.items():
                text = _localise(description, language) or ""
                default_value = defaults.get(name)
                if default_value is not None:
                    text = f"{text} _(default: `{default_value}`)_" if text else f"Default: `{default_value}`"
                lines.append(f"| `{name}` | {text} |")
            lines.append("")

    output = data.get("_output")
    if isinstance(output, dict) and output:
        _add_section(lines, "Output")
        states = output.get("state_enum")
        if states:
            state_list = ", ".join(str(state) for state in states)
            lines.append(f"- **States:** `{state_list}`")
        description = _localise(output.get("description"), language)
        if description:
            lines.append(f"- **Description:** {description}")
        payload = output.get("payload_schema_ref")
        if payload:
            lines.append(f"- **Payload schema:** `{payload}`")
        if states or description or payload:
            lines.append("")
        examples = output.get("examples")
        if isinstance(examples, dict) and examples:
            lines.append("### Output examples")
            lines.append("")
            for example_name, example_value in examples.items():
                lines.append(f"#### {example_name.replace('_', ' ').title()}")
                lines.append("```yaml")
                lines.append(_format_yaml_block(example_value))
                lines.append("```")
                lines.append("")

    errors = data.get("_errors")
    if isinstance(errors, dict) and errors:
        _add_section(lines, "Error handling")
        for severity, entries in errors.items():
            if not entries:
                continue
            lines.append(f"### {severity.title()}")
            lines.append("")
            for entry in entries:
                code = entry.get("code")
                when_text = _localise(entry.get("when"), language)
                if code and when_text:
                    lines.append(f"- `{code}` — {when_text}")
                elif code:
                    lines.append(f"- `{code}`")
                elif when_text:
                    lines.append(f"- {when_text}")
            lines.append("")

    examples = data.get("_examples")
    if isinstance(examples, dict) and examples:
        _add_section(lines, "Usage examples")
        for name, snippet in examples.items():
            lines.append(f"### {name.replace('_', ' ').title()}")
            lines.append("```yaml")
            lines.append(textwrap.dedent(str(snippet)).strip())
            lines.append("```")
            lines.append("")

    orchestrations = data.get("_orchestrations")
    if isinstance(orchestrations, Iterable):
        orchestrations = list(orchestrations)
        if orchestrations:
            _add_section(lines, "Orchestrations")
            for entry in orchestrations:
                if not isinstance(entry, dict):
                    continue
                name = entry.get("name") or "Example"
                lines.append(f"### {name}")
                snippet = entry.get("snippet")
                file_ref = entry.get("file")
                if snippet:
                    lines.append("```yaml")
                    lines.append(textwrap.dedent(str(snippet)).strip())
                    lines.append("```")
                if file_ref:
                    lines.append(f"File reference: `{file_ref}`")
                lines.append("")

    notes = data.get("_notes")
    if isinstance(notes, Iterable):
        note_list = [note for note in notes if isinstance(note, dict)]
        if note_list:
            _add_section(lines, "Notes")
            for note in note_list:
                text = _localise(note, language)
                if text:
                    lines.append(f"- {text}")
            lines.append("")

    related = data.get("_related")
    if isinstance(related, Iterable):
        related_list = [item for item in related if isinstance(item, str)]
        if related_list:
            _add_section(lines, "Related pipes")
            for item in related_list:
                lines.append(f"- `{item}`")
            lines.append("")

    return "\n".join(line.rstrip() for line in lines).rstrip() + "\n"


def _iter_sidecar_files(sidecar_dir: Path) -> list[Path]:
    if sidecar_dir.is_file() and sidecar_dir.suffix in {".yml", ".yaml"}:
        return [sidecar_dir]
    return sorted(sidecar_dir.rglob("*.yml")) + sorted(sidecar_dir.rglob("*.yaml"))


def generate_pipe_docs(
    sidecar_dir: Path,
    output_root: Path,
    languages: Sequence[str] = ("en",),
    source_root: Path | None = None,
    section_dir: Path = Path("developers/api/pipes"),
    project_root: Path | None = None,
) -> list[Path]:
    """Generate Markdown documentation for sidecars."""

    sidecar_dir = _ensure_absolute(sidecar_dir)
    output_root = _ensure_absolute(output_root)
    if source_root is None:
        source_root = _ensure_absolute(Path(__file__).resolve().parents[3] / "src")
    else:
        source_root = _ensure_absolute(source_root)
    project_root = _ensure_absolute(project_root or source_root.parent)

    generated: list[Path] = []
    for sidecar_path in _iter_sidecar_files(sidecar_dir):
        raw = yaml.safe_load(sidecar_path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict) or "_class" not in raw:
            continue
        code_ref = _resolve_code_reference(raw.get("_class", ""), source_root)
        slug_source = _localise(raw.get("_title"), languages[0]) if languages else None
        slug = _slugify(slug_source or code_ref.class_name)
        for language in languages:
            lang_dir = output_root / language / section_dir
            lang_dir.mkdir(parents=True, exist_ok=True)
            markdown = _build_markdown(raw, code_ref, language, project_root, sidecar_path)
            output_path = lang_dir / f"{slug}.md"
            output_path.write_text(markdown, encoding="utf-8")
            generated.append(output_path)
    return generated


app = typer.Typer(help="Generate VitePress documentation from pipe sidecars.")


@app.command()
def main(
    sidecar_dir: Path = typer.Argument(
        Path(__file__).resolve().parents[3] / "docs" / "man_structured" / "pipes",
        help="Directory containing pipe sidecar YAML files.",
    ),
    output_root: Path = typer.Option(
        Path(__file__).resolve().parents[3] / "docs" / "vitepress_docs" / "docs_src",
        "--output-root",
        "-o",
        help="Root directory that contains the per-language VitePress docs.",
    ),
    language: list[str] = typer.Option(
        ["en"],
        "--lang",
        "-l",
        help="Language codes to generate. Defaults to English only.",
    ),
    section: Path = typer.Option(
        Path("developers/api/pipes"),
        "--section",
        help="Relative path inside each language folder where the docs will be written.",
    ),
    source_root: Path | None = typer.Option(
        None,
        "--source-root",
        help="Root directory of the Python source tree (defaults to '<project>/src').",
    ),
) -> None:
    """Generate Markdown documentation for all discovered pipe sidecars."""

    generated = generate_pipe_docs(
        sidecar_dir=sidecar_dir,
        output_root=output_root,
        languages=language,
        source_root=source_root,
        section_dir=section,
    )
    typer.echo(f"Generated {len(generated)} file(s).")


if __name__ == "__main__":
    app()
