# src/duck_ytd_from_csv.py
import argparse
from pathlib import Path

import duckdb  # pip install duckdb


def main():
    p = argparse.ArgumentParser("Load facts.csv to DuckDB and produce YTD outputs")
    p.add_argument("--csv", required=True, help="Path to facts.csv")
    p.add_argument("--db", required=True, help="DuckDB file (will be created if missing)")
    p.add_argument("--out", required=True, help="Output folder for CSV exports")
    args = p.parse_args()

    csv_path = Path(args.csv)
    db_path = Path(args.db)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(db_path))

    # 1) Načítaj CSV do tabuľky facts (idempotentne)
    con.execute(
        """
        CREATE OR REPLACE TABLE facts AS
        SELECT *
        FROM read_csv_auto(?, HEADER=TRUE)
    """,
        [str(csv_path)],
    )
    # 2) Zisti dostupné stĺpce a poskladaj normalizačný SELECT
    cols = [r[1] for r in con.execute("PRAGMA table_info('facts')").fetchall()]

    select_list = """
        country,
        TRY_CAST(REGEXP_REPLACE(CAST(week AS VARCHAR), '^\\D+', '') AS INTEGER) AS week_int,
        metric,
        CAST(value AS DOUBLE) AS value
    """
    select_list += ", business" if "business" in cols else ", NULL AS business"
    select_list += ", source_file" if "source_file" in cols else ", NULL AS source_file"

    con.execute(
        f"""
        CREATE OR REPLACE VIEW facts_norm AS
        SELECT {select_list}
        FROM facts
    """
    )

    # 3) YTD kumulatívne po týždňoch
    con.execute(
        """
        CREATE OR REPLACE VIEW ytd_by_week AS
        SELECT
            country,
            business,
            metric,
            week_int AS week,
            SUM(value)                           AS week_value,
            SUM(SUM(value)) OVER (
                PARTITION BY country, business, metric
                ORDER BY week_int
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            )                                    AS ytd_value
        FROM facts_norm
        WHERE week_int IS NOT NULL
        GROUP BY country, business, metric, week_int
        ORDER BY country, business, metric, week_int
    """
    )

    # 4) YTD total (posledný dostupný týždeň za každú skupinu)
    con.execute(
        """
        CREATE OR REPLACE VIEW ytd_total AS
        SELECT t.country, t.business, t.metric, t.week, t.ytd_value
        FROM (
            SELECT
                country, business, metric,
                week,
                ytd_value,
                ROW_NUMBER() OVER (PARTITION BY country, business, metric ORDER BY week DESC) AS rn
            FROM ytd_by_week
        ) t
        WHERE t.rn = 1
        ORDER BY country, business, metric
    """
    )

    # 5) Exporty
    con.execute(f"COPY ytd_by_week TO '{out_dir / 'ytd_by_week.csv'}' (HEADER, DELIMITER ',')")
    con.execute(f"COPY ytd_total   TO '{out_dir / 'ytd_total.csv'}' (HEADER, DELIMITER ',')")
    print(f"✔ Loaded into: {db_path}")
    print(f"✔ Exported:    {out_dir / 'ytd_by_week.csv'}")
    print(f"✔ Exported:    {out_dir / 'ytd_total.csv'}")


if __name__ == "__main__":
    main()
