from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from src.io_duckdb import save_to_duckdb


@dataclass
class ExportConfig:
    db_path: str
    table: str
    mode: str = "append"


def export_to_duckdb(df: pd.DataFrame, config: ExportConfig) -> None:
    """Export normalized rows to DuckDB using shared IO helper."""
    if df.empty:
        return
    save_to_duckdb(df, db_path=config.db_path, table=config.table, mode=config.mode)
