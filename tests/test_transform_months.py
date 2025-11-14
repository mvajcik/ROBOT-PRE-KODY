# tests/test_transform_months.py
import numpy as np
import pandas as pd

from src.transform import transform_block


def test_transform_block_months_minimal():
    # Mini blok: 1 metrika, 2 mesiace (Jan = 200, Feb = "x" -> non-numeric -> MISSING + audit)
    block = {
        "cells": [
            {"row": 5, "col": 1, "value": "Turnover_EUR", "a1": "B6"},  # stĺpec 1 = Metric
            {"row": 5, "col": 2, "value": "200", "a1": "C6"},  # Jan
            {"row": 5, "col": 3, "value": "x", "a1": "D6"},  # Feb (chybné)
        ],
        "headers": {
            "static": {"Metric": 1},
            "months": [
                {"col": 2, "label": "Jan"},
                {"col": 3, "label": "Feb"},
            ],
        },
        "meta": {"country_hint": "SK", "business_hint": "WR", "block_id": "blk-m-001"},
        "fixes": {},
        "fallback_map": {},
    }

    data, audit = transform_block(block)

    # Očakávané 2 riadky: Jan=200.0 OK, Feb=MISSING
    expected = pd.DataFrame(
        [
            {
                "Country": "SK",
                "Business": "WR",
                "Metric": "Turnover_EUR",
                "PeriodType": "MONTH",
                "Period": "Jan",
                "Value": 200.0,
                "SourceBlockID": "blk-m-001",
                "QualityFlag": "OK",
                "Notes": "",
            },
            {
                "Country": "SK",
                "Business": "WR",
                "Metric": "Turnover_EUR",
                "PeriodType": "MONTH",
                "Period": "Feb",
                "Value": np.nan,
                "SourceBlockID": "blk-m-001",
                "QualityFlag": "MISSING",
                "Notes": "non-numeric",
            },
        ]
    )
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

    pd.testing.assert_frame_equal(data, expected, check_dtype=False, check_like=True)

    # Audit: 1 varovanie na Feb
    assert len(audit) == 1
    warn = audit.iloc[0].to_dict()
    assert warn["level"] == "WARN"
    assert warn["block_id"] == "blk-m-001"
    assert warn["metric"] == "Turnover_EUR"
    assert warn["period"] == "Feb"
    assert "Non-numeric" in warn["detail"]
