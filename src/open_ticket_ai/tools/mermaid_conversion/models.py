from dataclasses import dataclass
from typing import Self


@dataclass
class EdgeDef:
    source: str
    target: str
    label: str | None = None

@dataclass
class SubgraphDef:
    identifier: str
    label: str
    nodes: list[str]
    children: list[Self]
