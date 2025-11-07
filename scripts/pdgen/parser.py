from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ClassInfo:
    name: str
    bases: list[str]
    module: str
    has_decorator: bool
    file_path: str


class ClassVisitor(ast.NodeVisitor):
    def __init__(self, module_name: str, file_path: str) -> None:
        self.classes: list[ClassInfo] = []
        self.module_name = module_name
        self.file_path = file_path

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        has_decorator = any(
            (isinstance(dec, ast.Name) and dec.id == "include_in_uml")
            or (isinstance(dec, ast.Attribute) and dec.attr == "include_in_uml")
            for dec in node.decorator_list
        )

        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(f"{ast.unparse(base.value)}.{base.attr}")

        class_info = ClassInfo(
            name=node.name,
            bases=bases,
            module=self.module_name,
            has_decorator=has_decorator,
            file_path=self.file_path,
        )
        self.classes.append(class_info)
        self.generic_visit(node)


def parse_python_file(file_path: Path) -> list[ClassInfo]:
    try:
        with file_path.open("r", encoding="utf-8") as f:
            content = f.read()
        tree = ast.parse(content, filename=str(file_path))

        parts = file_path.parts
        module_parts: list[str]
        if "src" in parts:
            src_idx = parts.index("src")
            module_parts = list(parts[src_idx + 1 : -1])
        elif "packages" in parts:
            pkg_idx = parts.index("packages")
            module_parts = list(parts[pkg_idx + 2 : -1])
        else:
            module_parts = []

        module_name = ".".join(module_parts) if module_parts else "__main__"

        visitor = ClassVisitor(module_name, str(file_path))
        visitor.visit(tree)
        return visitor.classes
    except (OSError, SyntaxError):
        return []


def parse_python_files(root_path: Path) -> list[ClassInfo]:
    all_classes: list[ClassInfo] = []
    for py_file in root_path.rglob("*.py"):
        if "test" not in str(py_file) and ".venv" not in str(py_file):
            classes = parse_python_file(py_file)
            all_classes.extend(classes)
    return all_classes
