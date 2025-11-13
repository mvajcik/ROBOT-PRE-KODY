# src/tools/block_maker.py
from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd


def block_from_wide(values: pd.DataFrame, *, meta: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prevedie wide DF (index=Metric, columns = period labels) do block formátu,
    ktorý očakáva transform_block().
    - Predpoklad: columns sú týždne/mesiace atď. (napr. 'W1','Week 2','2025-W03','Jan','2025-01'…)
    - Vytvoríme headers.weeks ak stĺpce vyzerajú ako 'W...' alebo 'YYYY-W..', inak dáme months ak sú 'Jan.../01/2025-01'.
    """
    # zabezpeč index = Metric
    if values.index.name is None:
        values.index.name = "Metric"

    # urči typ období veľmi jednoducho (na test): ak väčšina stĺpcov začína na 'W' alebo obsahuje 'W'
    labels = list(map(str, values.columns))
    week_like = sum(1 for c in labels if ("W" in c.upper()))
    month_like = sum(1 for c in labels if ("Q" not in c.upper() and "H" not in c.upper() and "W" not in c.upper()))

    if week_like >= max(1, len(labels)//2):
        period_type = "WEEK"
        items = [{"col": i+2, "label": lbl} for i, lbl in enumerate(labels)]  # +2, lebo 'Metric' bude v col=1
        headers = {"static": {"Metric": 1}, "weeks": items}
    else:
        period_type = "MONTH"
        items = [{"col": i+2, "label": lbl} for i, lbl in enumerate(labels)]
        headers = {"static": {"Metric": 1}, "months": items}

    # buňky
    cells: List[Dict[str, Any]] = []
    for r_idx, (metric, row) in enumerate(values.iterrows(), start=2):  # riadok 1 bude header, riadok 2 prvá metrika
        # metric name cell (aby sme vedeli nájsť riadky metrík)
        cells.append({"row": r_idx, "col": 1, "value": str(metric)})
        # period values
        for c_off, lbl in enumerate(labels, start=2):
            cells.append({"row": r_idx, "col": c_off, "value": row[lbl]})

    block = {
        "meta": {
            "country_hint": meta.get("country", "UNKNOWN"),
            "business_hint": meta.get("business", "UNKNOWN"),
            "year": meta.get("year"),
            "block_id": meta.get("block_id", "ad-hoc"),
        },
        "headers": headers,
        "cells": cells,
    }
    return block