from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer

from robot_cli.validate import validate_scan_csv

app = typer.Typer(help="WR toolbox: scan, validate, build-ytd, build-stock (v0.4)")

@app.command("validate")
def validate(
    csv: Path = typer.Option(
        Path("data_out/scan__mini__AT_YTD.csv"),
        "--csv",
        help="Cesta k CSV výstupu zo scanu",
    )
):
    """Validuje CSV zo scanu (tolerantná Pandera schéma)."""
    code = validate_scan_csv(csv)
    raise typer.Exit(code)

# --- sub-app len pre 'scan' ---
scan_app = typer.Typer(help="Blok skenovania")

@scan_app.callback(invoke_without_command=True)
def scan(
    file: Path = typer.Option(..., "--file", "-f", exists=True, readable=True, help="Vstupný Excel"),
    sheet: str = typer.Option(..., "--sheet", "-s", help="Názov hárku"),
    cell_range: str = typer.Option(..., "--range", "-r", help="Excel range, napr. B2:E10"),
    out: Optional[Path] = typer.Option(None, "--out", "-o", help="Výstupné CSV"),
):
    """Spustí existujúci skener (src.osm_robot.robot) a uloží CSV do data_out/."""
    out_path = out or Path("data_out") / f"scan__{file.stem.replace(' ', '_')}__{sheet.replace(' ', '_')}.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
    sys.executable, "-m", "osm_robot.robot",   # ← bolo "src.osm_robot.robot"
    "--file", str(file), "--sheet", sheet, "--range", cell_range, "--out", str(out_path),
  ]
    typer.echo(f"→ Spúšťam: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        if res.stderr:
            typer.echo(res.stderr)
        raise typer.Exit(code=res.returncode)
    if res.stdout.strip():
        typer.echo(res.stdout.strip())
    typer.echo(f"✔ Hotovo: {out_path}")

# zaregistrujeme skupinu 'scan' pod root app
app.add_typer(scan_app, name="scan")

def main():
    app()

if __name__ == "__main__":
    app()