from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


@dataclass
class LoadedBlock:
    """Reprezentuje nahratý blok zo skenera pripravený na validáciu a transformáciu."""

    raw_block: Dict[str, Any]
    cells: List[Dict[str, Any]]
    headers: Dict[str, Any]
    meta: Dict[str, Any]
    country: str
    business: str
    block_id: str
    period_sets: List[Tuple[str, List[Dict[str, Any]]]]
    cell_map: Dict[Tuple[int, int], Any]


def load_block(block: Dict[str, Any]) -> LoadedBlock:
    """
    Loader ešte NIE JE napojený na transform_block.
    Zatiaľ len kopíruje existujúcu logiku: vytiahne cells, headers, meta,
    pripraví period_sets a cell_map.

    Neskôr ho prepojíme s transform_block a pridáme samostatný validator.
    """
    cells = block.get("cells") or []
    headers = block.get("headers") or {}
    meta = block.get("meta", {}) or {}

    country = meta.get("country_hint", "UNKNOWN")
    business = meta.get("business_hint", "UNKNOWN")
    block_id = meta.get("block_id", "NA")

    period_sets: List[Tuple[str, List[Dict[str, Any]]]] = []
    if headers.get("weeks"):
        period_sets.append(("WEEK", headers["weeks"]))
    if headers.get("months"):
        period_sets.append(("MONTH", headers["months"]))
    if headers.get("quarters"):
        period_sets.append(("QUARTER", headers["quarters"]))
    if headers.get("halves"):
        period_sets.append(("HALF", headers["halves"]))

    cell_map: Dict[Tuple[int, int], Any] = {}
    for c in cells:
        cell_map[(c["row"], c["col"])] = c.get("value", None)

    return LoadedBlock(
        raw_block=block,
        cells=cells,
        headers=headers,
        meta=meta,
        country=country,
        business=business,
        block_id=block_id,
        period_sets=period_sets,
        cell_map=cell_map,
    )
