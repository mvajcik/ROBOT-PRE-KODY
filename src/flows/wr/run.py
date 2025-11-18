from __future__ import annotations

import json
from pathlib import Path

from src.pipeline.exporter import ExportConfig
from src.pipeline.run_pipeline import run_pipeline


def run_wr_demo():
    """Run minimal WR block demo."""
    block_path = Path("data_in/mock_wr_block.json")
    with block_path.open() as f:
        block = json.load(f)

    export = ExportConfig(
        db_path="data_stage/wr_demo.duckdb",
        table="wr_blocks",
        mode="replace",
    )

    df, audit, issues = run_pipeline(block, export=export)
    print("WR demo → rows:", len(df), "| issues:", len(issues))


def run_wr_total_demo():
    """Run minimal WR TOTAL demo."""
    block_path = Path("data_in/mock_wr_total_block.json")
    with block_path.open() as f:
        block = json.load(f)

    export = ExportConfig(
        db_path="data_stage/wr_total_demo.duckdb",
        table="wr_total_blocks",
        mode="replace",
    )

    df, audit, issues = run_pipeline(block, export=export)
    print("WR TOTAL demo → rows:", len(df), "| issues:", len(issues))


if __name__ == "__main__":
    run_wr_demo()
    run_wr_total_demo()
