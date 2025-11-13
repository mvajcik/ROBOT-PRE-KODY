# src/wr_cli/validate.py
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

# odporúčaný import pre Pandera 0.26+
import pandera.pandas as pa
from pandera.errors import SchemaErrors


def _schema_for(df: pd.DataFrame) -> pa.DataFrameSchema:
    """
    Tolerantná schéma:
    - ak nájde typické stĺpce zo scanu (row, col, address, value), skontroluje typy,
    - inak aspoň overí, že CSV nie je prázdne.
    """
    cols = {c.lower(): c for c in df.columns}

    schema_cols: dict[str, pa.Column] = {}
    if "row" in cols:
        schema_cols[cols["row"]] = pa.Column(int, checks=pa.Check.ge(1), nullable=False, coerce=True)
    if "col" in cols:
        schema_cols[cols["col"]] = pa.Column(int, checks=pa.Check.ge(1), nullable=False, coerce=True)
    if "address" in cols:
        schema_cols[cols["address"]] = pa.Column(str, nullable=False, coerce=True)
    if "value" in cols:
        # povolíme rôzne typy hodnôt, ale nie NaN
        schema_cols[cols["value"]] = pa.Column(object, nullable=False)

    if schema_cols:
        return pa.DataFrameSchema(schema_cols)

    # fallback: aspoň nech má dáta (min. 1 riadok)
    return pa.DataFrameSchema(
        {df.columns[0]: pa.Column(object)},
        checks=pa.Check(lambda d: len(d) >= 1, error="CSV je prázdne."),
    )


def validate_scan_csv(csv_path: Path) -> int:
    p = Path(csv_path)
    if not p.exists():
        print(f"❌ Súbor neexistuje: {p}", file=sys.stderr)
        return 2

    try:
        df = pd.read_csv(p)
    except Exception as e:
        print(f"❌ Neviem načítať CSV: {p}\n{e}", file=sys.stderr)
        return 2

    schema = _schema_for(df)

    try:
        _ = schema.validate(df, lazy=True)
    except SchemaErrors as err:
        print("❌ Validácia zlyhala (Pandera):")
        failures = err.failure_cases
        print(f"- Počet chýb: {len(failures)}")
        print(failures.head(20).to_string(index=False))
        return 1

    print("✔ Validácia prebehla úspešne (Pandera).")
    print(f"• Riadkov: {len(df)}, Stĺpcov: {len(df.columns)}")
    return 0