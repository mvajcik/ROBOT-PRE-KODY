# tests/test_transform.py
import numpy as np
import pandas as pd

from src.transform import transform_block


def test_transform_block_weeks_minimal():
    # --- Mini vstupný blok (ako by ho dodal scanner) ---
    block = {
        "cells": [
            # Riadok 10: názov metriky
            {"row": 10, "col": 1, "value": "Turnover_EUR", "a1": "B11"},
            # Hodnoty týždňov pre ten istý riadok
            {"row": 10, "col": 2, "value": "100", "a1": "C11"},  # W1 - numeric
            {
                "row": 10,
                "col": 3,
                "value": "abc",
                "a1": "D11",
            },  # W2 - non-numeric (má ísť do audit)
        ],
        "headers": {
            "static": {"Metric": 1},  # stĺpec s názvom metriky
            "weeks": [
                {"col": 2, "label": "W1"},
                {"col": 3, "label": "W2"},
            ],
        },
        "meta": {"country_hint": "SK", "business_hint": "WR", "block_id": "blk-001"},
        "fixes": {},
        "fallback_map": {},
    }

    data, audit = transform_block(block)

    # --- Očakávané dáta ---
    expected = pd.DataFrame(
        [
            {
                "Country": "SK",
                "Business": "WR",
                "Metric": "Turnover_EUR",
                "PeriodType": "WEEK",
                "Period": "W1",
                "Value": 100.0,
                "SourceBlockID": "blk-001",
                "QualityFlag": "OK",
                "Notes": "",
            },
            {
                "Country": "SK",
                "Business": "WR",
                "Metric": "Turnover_EUR",
                "PeriodType": "WEEK",
                "Period": "W2",
                "Value": np.nan,  # non-numeric -> None/NaN
                "SourceBlockID": "blk-001",
                "QualityFlag": "MISSING",
                "Notes": "non-numeric",
            },
        ]
    )

    # Pre porovnanie nastavíme jednotné poradie stĺpcov
    cols = [
        "Country",
        "Business",
        "Metric",
        "PeriodType",
        "Period",
        "Value",
        "SourceBlockID",
        "QualityFlag",
        "Notes",
    ]
    data = data.reindex(columns=cols).sort_values(by=["Period"]).reset_index(drop=True)
    expected = expected.reindex(columns=cols).sort_values(by=["Period"]).reset_index(drop=True)

    # Číselné NaN porovnávame ako ekvivalent None
    pd.testing.assert_frame_equal(data, expected, check_dtype=False, check_like=True)

    # --- Audit by mal mať 1 varovanie pre W2 (non-numeric) ---
    assert len(audit) == 1
    row = audit.iloc[0].to_dict()
    assert row["level"] == "WARN"
    assert row["block_id"] == "blk-001"
    assert row["metric"] == "Turnover_EUR"
    assert row["period"] == "W2"
    assert "Non-numeric" in row["detail"]
