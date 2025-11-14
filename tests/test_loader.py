from src.pipeline.loader import LoadedBlock, load_block


def test_load_block_basic_structure():
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
            "block_id": "TEST-BLOCK-1",
            "year": 2025,
        },
    }

    loaded = load_block(block)

    assert isinstance(loaded, LoadedBlock)
    assert loaded.cells == block["cells"]
    assert loaded.headers == block["headers"]
    assert loaded.meta["country_hint"] == "SVK"
    assert loaded.country == "SVK"
    assert loaded.business == "WR"
    assert loaded.block_id == "TEST-BLOCK-1"

    # period_sets by mali obsahovať jeden WEEK záznam
    assert len(loaded.period_sets) == 1
    period_type, items = loaded.period_sets[0]
    assert period_type == "WEEK"
    assert items[0]["label"] == "W1"

    # cell_map má mať kľúč (row, col) -> value
    assert loaded.cell_map[(1, 2)] == 123
