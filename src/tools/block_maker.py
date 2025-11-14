# src/tools/block_maker.py
from __future__ import annotations

from typing import Any

import pandas as pd


def make_block_from_df(values: pd.DataFrame) -> dict:
    """Build scanner-like block from wide DF (index=Metric, columns=period labels)."""
    # ensure index = Metric
    if values.index.name is None:
        values = values.copy()
        values.index.name = "Metric"

    # decide period type in a simple way
    labels = list(map(str, values.columns))
    week_like = sum(1 for c in labels if "W" in c.upper())

    if week_like >= len(labels) // 2:
        items = [{"col": i + 2, "label": lbl} for i, lbl in enumerate(labels)]
        headers = {"static": {"Metric": 1}, "weeks": items}
    else:
        items = [{"col": i + 2, "label": lbl} for i, lbl in enumerate(labels)]
        headers = {"static": {"Metric": 1}, "months": items}

    # cells
    cells: list[dict[str, Any]] = []
    for r_idx, (metric, row) in enumerate(values.iterrows(), start=2):
        cells.append({"row": r_idx, "col": 1, "value": metric})
        for c_idx, label in enumerate(labels, start=2):
            cells.append({"row": r_idx, "col": c_idx, "value": row[label]})

    return {
        "cells": cells,
        "headers": headers,
        "meta": {},
        "fixes": {},
        "fallback_map": {},
    }
