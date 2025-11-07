from __future__ import annotations

from scripts.pdgen.parser import ClassInfo


def generate_plantuml(classes: list[ClassInfo]) -> str:
    relevant_classes: set[str] = set()

    for cls in classes:
        if cls.has_decorator:
            relevant_classes.add(cls.name)

    changed = True
    while changed:
        changed = False
        for cls in classes:
            if cls.name not in relevant_classes and (
                any(base in relevant_classes for base in cls.bases)
                or any(c.name in relevant_classes and cls.name in c.bases for c in classes)
            ):
                relevant_classes.add(cls.name)
                changed = True

    lines = ["@startuml", ""]

    for cls in classes:
        if cls.name in relevant_classes:
            if cls.has_decorator:
                lines.append(f"class {cls.name} <<@include_in_uml>>")
            else:
                lines.append(f"class {cls.name}")

    lines.append("")

    for cls in classes:
        if cls.name in relevant_classes and cls.bases:
            lines.extend(
                f"{base} <|-- {cls.name}" for base in cls.bases if base in relevant_classes
            )

    lines.append("")
    lines.append("@enduml")
    return "\n".join(lines)


def _find_class_by_name(classes: list[ClassInfo], name: str) -> ClassInfo | None:
    for cls in classes:
        if cls.name == name or cls.name.endswith(f".{name}"):
            return cls
    return None
