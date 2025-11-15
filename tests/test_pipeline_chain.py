import pandas as pd

from src.pipeline.loader import load_block
from src.pipeline.validator import validate_block
from src.transform import transform_block


def test_pipeline_chain_minimal():
    # --- Minimal mock block (simulácia scannera) ---
    block = {
        "meta": {
            "country_hint": "SK",
            "business_hint": "Retail",
            "block_id": "B1",
            "year_hint": 2025,
        },
        "headers": {
            "static": {"Metric": 2},
            "weeks": [{"col": 3, "label": "W1"}],
        },
        "cells": [
            {"row": 1, "col": 2, "value": "Sales"},
            {"row": 1, "col": 3, "value": 100},
        ],
    }

    # --- Loader ---
    loaded = load_block(block)

    # --- Validator ---
    issues = validate_block(loaded)

    # --- Transform ---
    df, audit = transform_block(block)

    # --- Checks ---
    assert isinstance(df, pd.DataFrame)
    assert set(df.columns) == {
        "Country",
        "Business",
        "Metric",
        "PeriodType",
        "Period",
        "PeriodKey",
        "Value",
        "SourceBlockID",
        "QualityFlag",
        "Notes",
    }
    assert len(df) == 1

    assert isinstance(audit, pd.DataFrame)
    assert isinstance(issues, list)
