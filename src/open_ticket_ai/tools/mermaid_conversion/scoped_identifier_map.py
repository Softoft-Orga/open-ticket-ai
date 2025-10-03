from typing import Self


class ScopedIdentifierMap:
    def __init__(self, parent: Self | None = None) -> None:
        self.parent = parent
        self.values: dict[str, str] = {}
    def set_value(self, local_name: str, global_identifier: str) -> None:
        self.values[local_name] = global_identifier
    def resolve(self, name: str) -> str | None:
        if name in self.values:
            return self.values[name]
        if self.parent is not None:
            return self.parent.resolve(name)
        return None
