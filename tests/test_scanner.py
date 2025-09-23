from pathlib import Path
from src.scanner import scan_block

# tests/test_scanner.py
from pathlib import Path
from src.scanner import scan_block_legacy

def test_scan_block_basic():
    xlsx = Path("tests/fixtures/mini.xlsx")
    cells = scan_block_legacy(
        xlsx,
        sheet="AT_YTD",
        top_left="B2",
        bottom_right="E6"
    )

    # základné overenia
    assert isinstance(cells, list)
    assert len(cells) > 0

    sample = cells[0]
    assert {"row", "col", "address", "value"} <= set(sample.keys())
