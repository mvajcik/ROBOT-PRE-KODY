from __future__ import annotations

from pathlib import Path

import duckdb


def export_weekly_csv():
    db_path = "data_stage/wr_total_demo.duckdb"
    out_path = Path("data_out/wr_total_weekly_demo.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(db_path)
    try:
        df = con.execute(
            """
            SELECT
                Metric,
                SUM(CASE WHEN Period = 'W1' THEN Value END) AS W1,
                SUM(CASE WHEN Period = 'W2' THEN Value END) AS W2,
                SUM(CASE WHEN Period = 'W3' THEN Value END) AS W3
            FROM wr_total_blocks
            GROUP BY Metric
            """
        ).fetchdf()
    finally:
        con.close()

    df.to_csv(out_path, index=False)
    print("Saved:", out_path)


if __name__ == "__main__":
    export_weekly_csv()
