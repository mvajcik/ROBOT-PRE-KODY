# tests/test_transform_perf.py
import time

import pandas as pd

from src.transform import transform_block


def make_block(num_metrics=30, weeks=52):
    """
    Vytvorí syntetický 'scanner' blok s viacerými metrikami a týždňami.
    Každá metrika = 1 riadok: stĺpec Metric + 52 týždňov.
    Každý 10. týždeň naschvál vloží nečíselnú hodnotu (audit).
    """
    cells = []
    headers = {
        "static": {"Metric": 1},  # stĺpec 1 = názov metriky
        "weeks": [{"col": c, "label": f"W{c-1}"} for c in range(2, 2 + weeks)],  # col=2..53 -> W1..W52
    }
    meta = {"country_hint": "SK", "business_hint": "WR", "block_id": "blk-perf"}

    # Každá metrika na novom riadku
    for i in range(num_metrics):
        row = 10 + i  # ľubovoľné číslo riadku
        metric_name = f"Metric_{i+1}"
        cells.append({"row": row, "col": 1, "value": metric_name, "a1": f"B{row+1}"})

        for w_idx, week in enumerate(headers["weeks"], start=1):
            col = week["col"]
            # každá 10. hodnota bude nečíselná -> audit
            if w_idx % 10 == 0:
                val = "x"
            else:
                # napr. 100 * (i+1) + w_idx ako string (aby sa testol parse)
                val = str(100 * (i + 1) + w_idx)
            cells.append({"row": row, "col": col, "value": val, "a1": "X"})

    return {
        "cells": cells,
        "headers": headers,
        "meta": meta,
        "fixes": {},
        "fallback_map": {},
    }

def test_transform_block_perf_medium():
    block = make_block(num_metrics=30, weeks=52)

    t0 = time.perf_counter()
    data, audit = transform_block(block)
    dt = time.perf_counter() - t0

    # Očakávaný počet riadkov = metriky * týždne
    expected_rows = 30 * 52
    assert len(data) == expected_rows

    # Počet audit záznamov = každá 10. bunka je non-numeric
    # t.j. na metrikách: floor(52/10) * 30
    expected_audit = (52 // 10) * 30
    assert len(audit) == expected_audit

    # Kontrola niekoľkých vzoriek
    sample = data[(data["Metric"] == "Metric_1") & (data["Period"] == "W1")].iloc[0]
    assert sample["Value"] == 101.0  # 100*(1) + 1

    # Každý 10. týždeň je MISSING
    missing = data[(data["Metric"] == "Metric_1") & (data["Period"] == "W10")].iloc[0]
    assert pd.isna(missing["Value"]) and missing["QualityFlag"] == "MISSING"

    # Hrubý, ale priaznivý limit na stredne veľký vstup (30x52)
    # Cieľ: nech je to "rýchle dosť" na bežné iterovanie pri vývoji.
    assert dt < 3.0, f"Transform je pomalá na medium vstupe: {dt:.3f}s"