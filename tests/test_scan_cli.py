# tests/test_scan_cli.py
import csv
from pathlib import Path

from src.scanner import scan_block

FIXT = Path("tests/fixtures")
GOLD = Path("tests/golden")


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.reader(f))


def test_scan_block_csv(tmp_path):
    # vstup
    xlsx = FIXT / "mini.xlsx"
    sheet = "AT_YTD"
    rng = "B2:E6"

    # výstup do dočasného priečinka
    out_csv = tmp_path / "scan.csv"
    scan_block(str(xlsx), sheet, rng, str(out_csv))

    got = read_csv(out_csv)
    exp = read_csv(GOLD / "mini_cells_B2_E6.csv")

    assert got[0] == ["sheet", "row", "col", "value", "formula"]
    assert exp[0] == ["sheet", "row", "col", "value", "formula"]
    assert got == exp
