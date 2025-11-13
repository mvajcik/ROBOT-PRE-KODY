from src.transform import transform_block


def test_period_normalization_quarters_halves_with_year_hint():
    block = {
        "cells": [
            {"row": 4, "col": 1, "value": "Inventory_EUR", "a1": "B5"},
            {"row": 4, "col": 2, "value": "1000", "a1": "C5"},  # Q1
            {"row": 4, "col": 3, "value": "2000", "a1": "D5"},  # H2
        ],
        "headers": {
            "static": {"Metric": 1},
            "quarters": [{"col": 2, "label": "Q1"}],
            "halves":   [{"col": 3, "label": "H2"}],
        },
        "meta": {"country_hint": "SK", "business_hint": "WR", "block_id": "blk-qh-001", "year_hint": 2025},
        "fixes": {},
        "fallback_map": {},
    }

    data, audit = transform_block(block)
    assert "PeriodKey" in data.columns

    # skontroluj podľa typu
    q = data[data["PeriodType"] == "QUARTER"].iloc[0]
    h = data[data["PeriodType"] == "HALF"].iloc[0]
    assert q["Period"] == "Q1" and q["PeriodKey"] == "2025-Q1"
    assert h["Period"] == "H2" and h["PeriodKey"] == "2025-H2"
    assert audit.empty