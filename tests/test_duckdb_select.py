import duckdb

from src.io_duckdb import save_to_duckdb
from src.transform import transform_block


def test_duckdb_ytd_sum(tmp_path):
    # 1) priprav blok s dvoma týždňami
    block = {
        "cells": [
            {"row": 1, "col": 1, "value": "Turnover_EUR"},
            {"row": 1, "col": 2, "value": "100"},  # W1
            {"row": 1, "col": 3, "value": "200"},  # W2
        ],
        "headers": {
            "static": {"Metric": 1},
            "weeks": [
                {"col": 2, "label": "W1"},
                {"col": 3, "label": "W2"},
            ],
        },
        "meta": {
            "country_hint": "SK",
            "business_hint": "WR",
            "block_id": "blk-ytd-001",
            "year_hint": 2025,
        },
        "fixes": {},
        "fallback_map": {},
    }

    df, audit = transform_block(block)
    assert audit.empty

    # 2) zapíš do DuckDB
    db_path = str(tmp_path / "ytd.duckdb")
    save_to_duckdb(df, db_path, "fact_metrics", mode="replace")

    # 3) SELECT – YTD SUM
    con = duckdb.connect(db_path)
    try:
        result = con.execute("""
            SELECT Metric, SUM(Value) AS YTD
            FROM fact_metrics
            WHERE Country = 'SK' AND Business = 'WR'
            GROUP BY Metric
        """).fetchdf()
    finally:
        con.close()

    # 4) očakávaný výsledok = 100 + 200 = 300
    assert result.iloc[0]["Metric"] == "Turnover_EUR"
    assert result.iloc[0]["YTD"] == 300.0