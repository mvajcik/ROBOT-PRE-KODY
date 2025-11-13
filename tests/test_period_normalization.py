from src.transform import transform_block


def test_period_normalization_months_with_year_hint():
    block = {
        "cells": [
            {"row": 5, "col": 1, "value": "Turnover_EUR", "a1": "B6"},
            {"row": 5, "col": 2, "value": "200", "a1": "C6"},  # Jan
            {"row": 5, "col": 3, "value": "300", "a1": "D6"},  # Feb
        ],
        "headers": {
            "static": {"Metric": 1},
            "months": [
                {"col": 2, "label": "Jan"},
                {"col": 3, "label": "Feb"},
            ],
        },
        "meta": {"country_hint": "SK", "business_hint": "WR", "block_id": "blk-m-002", "year_hint": 2025},
        "fixes": {},
        "fallback_map": {},
    }

    data, audit = transform_block(block)
    assert "PeriodKey" in data.columns

    # skontroluj normalizované kľúče
    by_period = dict(zip(data["Period"], data["PeriodKey"]))
    assert by_period["Jan"] == "2025-01"
    assert by_period["Feb"] == "2025-02"

    # ostatné polia ostávajú nedotknuté
    assert set(data["PeriodType"]) == {"MONTH"}
    assert audit.empty