from src.pipeline.loader import load_block
from src.pipeline.validator import ValidationIssue, validate_block


def test_validate_block_returns_empty_list_for_basic_block():
    block = {
        "cells": [
            {"row": 1, "col": 1, "value": "Metric 1"},
            {"row": 1, "col": 2, "value": 123},
        ],
        "headers": {
            "static": {"Metric": 1},
            "weeks": [{"col": 2, "label": "W1"}],
        },
        "meta": {
            "country_hint": "SVK",
            "business_hint": "WR",
            "block_id": "VAL-TEST-1",
            "year": 2025,
        },
    }

    loaded = load_block(block)
    issues = validate_block(loaded)

    assert isinstance(issues, list)
    assert all(isinstance(i, ValidationIssue) for i in issues)
    # zatiaľ neočakávame žiadne problémy
    assert issues == []
