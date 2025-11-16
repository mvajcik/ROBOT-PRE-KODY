from src.pipeline.loader import load_block
from src.pipeline.transformer import TransformResult, transform_loaded_block


def test_transform_loaded_block_contract_minimal():
    block = {
        "cells": [],
        "headers": {},
        "meta": {"country_hint": "SK", "business_hint": "WR", "block_id": "blk-test"},
        "fixes": {},
        "fallback_map": {},
    }

    loaded = load_block(block)
    result = transform_loaded_block(loaded)

    assert isinstance(result, TransformResult)
    assert isinstance(result.rows, list)
    assert isinstance(result.audit_rows, list)
