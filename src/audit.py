# ruff: noqa: E501
# src/audit.py
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Dict, List, Tuple

Row = Dict[str, str]


def load_cellmap(csv_path: Path) -> List[Row]:
    with csv_path.open(newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        return list(rdr)


def parse_float(x: str) -> float:
    if x is None or x == "":
        return 0.0
    try:
        return float(str(x).replace(" ", "").replace(",", "."))
    except ValueError:
        return 0.0


def sum_block(rows: List[Row], row_min: int, row_max: int, cols: List[str]) -> float:
    cols_set = {c.upper() for c in cols}
    total = 0.0
    for r in rows:
        try:
            rr = int(r["row"])
        except Exception:
            continue
        if row_min <= rr <= row_max and r.get("col", "").upper() in cols_set:
            total += parse_float(r.get("value", ""))
    return total


def get_cell_value(rows: List[Row], row: int, col: str) -> float:
    col_u = col.upper()
    for r in rows:
        try:
            if int(r.get("row", -1)) == row and r.get("col", "").upper() == col_u:
                return parse_float(r.get("value", ""))
        except Exception:
            continue
    return 0.0


def audit_sum_equals_total(
    rows: List[Row],
    *,
    sum_rows: Tuple[int, int],
    sum_cols: List[str],
    total_cell: Tuple[int, str],
) -> Tuple[bool, str]:
    s = sum_block(rows, sum_rows[0], sum_rows[1], sum_cols)
    total = get_cell_value(rows, total_cell[0], total_cell[1])
    ok = abs(s - total) < 1e-9
    msg = f"[{'✔' if ok else '✖'}] SUM({sum_cols},{sum_rows[0]}:{sum_rows[1]})={s:.2f} vs TOTAL({total_cell[1]}{total_cell[0]})={total:.2f}"
    return ok, msg


def main() -> None:
    ap = argparse.ArgumentParser(description="Audit log over cell-map CSV.")
    ap.add_argument(
        "--csv", required=True, help="Path to cell-map CSV (sheet,row,col,value,formula)"
    )
    ap.add_argument("--out", default="data_out/audit.txt", help="Path to audit text log")
    ap.add_argument("--sum-rows", required=True, help="e.g. 2:6 (inclusive)")
    ap.add_argument("--sum-cols", required=True, help="Comma separated, e.g. B,C,D,E")
    ap.add_argument("--total-cell", required=True, help="e.g. I6 (col+row)")
    args = ap.parse_args()

    rows = load_cellmap(Path(args.csv))

    # 1) range riadkov
    try:
        r1, r2 = (int(x) for x in args.sum_rows.split(":"))
    except Exception as e:
        raise ValueError(
            f"--sum-rows musí byť vo formáte 'start:end', dostal som: {args.sum_rows!r}"
        ) from e

    # 2) zoznam stĺpcov
    cols = [c.strip().upper() for c in args.sum_cols.split(",") if c.strip()]

    # 3) total bunka (A1 -> col+row)
    m = re.fullmatch(r"([A-Za-z]+)(\d+)", args.total_cell.strip())
    if not m:
        raise ValueError(f"--total-cell musí byť ako A1, napr. I6. Dostalo sa: {args.total_cell!r}")
    col_total, row_total = m.group(1).upper(), int(m.group(2))

    ok, line = audit_sum_equals_total(
        rows,
        sum_rows=(r1, r2),
        sum_cols=cols,
        total_cell=(row_total, col_total),
    )

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("AUDIT LOG\n")
        f.write(line + "\n")

    print(line)
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
