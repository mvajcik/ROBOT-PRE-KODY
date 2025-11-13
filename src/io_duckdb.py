# src/io_duckdb.py
from __future__ import annotations

import duckdb


def save_to_duckdb(df, db_path: str, table: str, mode: str = "append") -> None:
    """
    Uloží DataFrame do DuckDB.
    mode="replace"  -> CREATE OR REPLACE TABLE ... AS SELECT * FROM df
    mode="append"   -> CREATE TABLE IF NOT EXISTS ...; INSERT INTO ...
    """
    con = duckdb.connect(db_path)
    try:
        con.register("df", df)
        if mode == "replace":
            con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM df")
        elif mode == "append":
            con.execute(f"CREATE TABLE IF NOT EXISTS {table} AS SELECT * FROM df WHERE 1=0")
            con.execute(f"INSERT INTO {table} SELECT * FROM df")
        else:
            raise ValueError("mode must be 'replace' or 'append'")
    finally:
        con.close()