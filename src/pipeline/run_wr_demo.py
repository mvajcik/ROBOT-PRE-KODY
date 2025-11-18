from __future__ import annotations

import json
from pathlib import Path

from src.pipeline.exporter import ExportConfig
from src.pipeline.run_pipeline import run_pipeline


def run():
    block_path = Path("data_in/mock_wr_block.json")
    with block_path.open() as f:
        block = json.load(f)

    export = ExportConfig(db_path="data_stage/wr_demo.duckdb", table="wr_blocks", mode="replace")

    df, audit, issues = run_pipeline(block, export=export)

    print("Rows:", len(df))
    print("Audit:", len(audit))
    print("Issues:", len(issues))
    print("Saved to:", export.db_path)


if __name__ == "__main__":
    run()
