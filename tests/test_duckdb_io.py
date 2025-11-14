# tests/test_duckdb_io.py
import duckdb

from src.io_duckdb import save_to_duckdb
from src.transform import transform_block


def test_save_to_duckdb_creates_table_and_writes_rows(tmp_path):
    # mini blok -> DataFrame
    block = {
        "cells": [
            {"row": 7, "col": 1, "value": "Turnover_EUR", "a1": "B8"},
            {"row": 7, "col": 2, "value": "100", "a1": "C8"},  # W1
            {"row": 7, "col": 3, "value": "200", "a1": "D8"},  # W2
        ],
        "headers": {
            "static": {"Metric": 1},
            "weeks": [{"col": 2, "label": "W1"}, {"col": 3, "label": "W2"}],
        },
        "meta": {
            "country_hint": "SK",
            "business_hint": "WR",
            "block_id": "blk-db-001",
            "year_hint": 2025,
        },
        "fixes": {},
        "fallback_map": {},
    }
    df, audit = transform_block(block)
    assert audit.empty

    db_path = str(tmp_path / "test.duckdb")
    table = "fact_metrics"

    # write (replace for idempotency)
    save_to_duckdb(df, db_path, table, mode="replace")

    # verify
    con = duckdb.connect(db_path)
    try:
        n = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        assert n == len(df)

        cols = [r[1] for r in con.execute(f"PRAGMA table_info('{table}')").fetchall()]
        for c in [
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
        ]:
            assert c in cols
    finally:
        con.close()
