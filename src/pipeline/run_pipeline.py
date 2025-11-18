from __future__ import annotations

from src.pipeline.exporter import ExportConfig, export_to_duckdb
from src.pipeline.loader import load_block
from src.pipeline.validator import validate_block
from src.transform import transform_block


def run_pipeline(block, *, export: ExportConfig | None = None):
    loaded = load_block(block)
    issues = validate_block(loaded)
    df, audit = transform_block(block)

    if export is not None:
        export_to_duckdb(df, export)

    return df, audit, issues
