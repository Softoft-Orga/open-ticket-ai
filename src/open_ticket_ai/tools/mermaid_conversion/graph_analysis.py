from __future__ import annotations
from typing import Iterable
from .models import EdgeDef

def collect_internal_roots(node_identifiers: list[str], edges: list[EdgeDef]) -> list[str]:
    indegree: dict[str, int] = {nid: 0 for nid in node_identifiers}
    for e in edges:
        if e.target in indegree:
            indegree[e.target] += 1
    return [nid for nid, d in indegree.items() if d == 0]

def collect_internal_sinks(node_identifiers: list[str], edges: list[EdgeDef]) -> list[str]:
    outdegree: dict[str, int] = {nid: 0 for nid in node_identifiers}
    for e in edges:
        if e.source in outdegree:
            outdegree[e.source] += 1
    return [nid for nid, d in outdegree.items() if d == 0]
