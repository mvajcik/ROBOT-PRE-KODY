from src.transform import transform_block


def test_period_normalization_weeks_with_year_hint():
    block = {
        "cells": [
            {"row": 7, "col": 1, "value": "Turnover_EUR", "a1": "B8"},
            {"row": 7, "col": 2, "value": "100", "a1": "C8"},   # W1
            {"row": 7, "col": 3, "value": "200", "a1": "D8"},   # W10
        ],
        "headers": {
            "static": {"Metric": 1},
            "weeks": [
                {"col": 2, "label": "W1"},
                {"col": 3, "label": "W10"},
            ],
        },
        "meta": {"country_hint": "SK", "business_hint": "WR", "block_id": "blk-w-001", "year_hint": 2025},
        "fixes": {},
        "fallback_map": {},
    }

    data, audit = transform_block(block)
    assert "PeriodKey" in data.columns
    by_period = dict(zip(data["Period"], data["PeriodKey"]))
    assert by_period["W1"]  == "2025-W01"
    assert by_period["W10"] == "2025-W10"
    assert set(data["PeriodType"]) == {"WEEK"}
    assert audit.empty