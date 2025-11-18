import duckdb
import pandas as pd

from src.pipeline.exporter import ExportConfig, export_to_duckdb


def test_export_to_duckdb_append(tmp_path):
    db_path = tmp_path / "test_export.duckdb"
    config = ExportConfig(db_path=str(db_path), table="t_export", mode="append")

    df = pd.DataFrame({"a": [1, 2]})
    export_to_duckdb(df, config)

    con = duckdb.connect(str(db_path))
    try:
        result = con.execute("SELECT COUNT(*) FROM t_export").fetchone()[0]
        assert result == 2
    finally:
        con.close()
