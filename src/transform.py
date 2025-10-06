import pandas as pd

# --- Normalizácia období pre DuckDB (bezpečná, neprepisuje pôvodný label) ---
def _normalize_period(period_type: str, label: str, year_hint=None) -> str | None:
    """
    Vráti normalizovaný kľúč obdobia (PeriodKey) alebo None, ak nevieme určiť rok/format.
    - WEEK:   'W1'..'W52'  -> 'YYYY-W01' (s nulovaním)
    - MONTH:  'Jan','February','1','01','2025-01' -> 'YYYY-01'
    - QUARTER:'Q1','2025-Q1' -> 'YYYY-Q1'
    - HALF:   'H1','2025-H1' -> 'YYYY-H1'
    Ak label už obsahuje rok vo formáte 'YYYY-..', vrátime ho tak ako je (po ľahkej kontrole).
    """
    if not label:
      return None

    # ak už je to tvar 'YYYY-...' nechaj tak
    if isinstance(label, str) and len(label) >= 5 and label[:4].isdigit() and label[4] == "-":
        return label

    # bez roka nevieme vytvoriť kľúč
    if not year_hint:
        return None

    try:
        y = int(year_hint)
    except Exception:
        return None

    t = period_type.upper()

    if t == "WEEK":
        # ak label = 'W7' alebo 'W07'
        s = str(label).strip().upper().lstrip()
        if s.startswith("W"):
            try:
                w = int(s[1:])
                return f"{y}-W{w:02d}"
            except Exception:
                return None
        # prípad '7'
        try:
            w = int(s)
            return f"{y}-W{w:02d}"
        except Exception:
            return None

    if t == "MONTH":
        m_map = {
            "JANUARY":1,"JAN":1,"01":1,"1":1,
            "FEBRUARY":2,"FEB":2,"02":2,"2":2,
            "MARCH":3,"MAR":3,"03":3,"3":3,
            "APRIL":4,"APR":4,"04":4,"4":4,
            "MAY":5,"05":5,"5":5,
            "JUNE":6,"JUN":6,"06":6,"6":6,
            "JULY":7,"JUL":7,"07":7,"7":7,
            "AUGUST":8,"AUG":8,"08":8,"8":8,
            "SEPTEMBER":9,"SEP":9,"SEPT":9,"09":9,"9":9,
            "OCTOBER":10,"OCT":10,"10":10,
            "NOVEMBER":11,"NOV":11,"11":11,
            "DECEMBER":12,"DEC":12,"12":12,
        }
        s = str(label).strip().upper()
        m = m_map.get(s)
        if m:
            return f"{y}-{m:02d}"
        return None

    if t == "QUARTER":
        s = str(label).strip().upper()
        if s.startswith("Q"):
            try:
                q = int(s[1:])
                if 1 <= q <= 4:
                    return f"{y}-Q{q}"
            except Exception:
                return None
        return None

    if t == "HALF":
        s = str(label).strip().upper()
        if s.startswith("H"):
            try:
                h = int(s[1:])
                if h in (1,2):
                    return f"{y}-H{h}"
            except Exception:
                return None
        return None

    return None


def transform_block(block: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    import pandas as pd  # (ak už nie je hore)

    # ---- SAFETY: ak príde prázdny vstup, vráť kontrakt so správnymi dtypes ----
    # ak je vstup DataFrame, voláme ho raw_df; ak je to iný typ (napr. dict z nášho skeneru), nechaj raw_df=None
    raw_df = block if isinstance(block, pd.DataFrame) else None

    if raw_df is None or (hasattr(raw_df, "empty") and raw_df.empty):
        out_df = pd.DataFrame({
            "Country": pd.Series(dtype="string"),
            "Week":    pd.Series(dtype="int64"),
            "Metric":  pd.Series(dtype="string"),
            "Value":   pd.Series(dtype="float64"),
        })
        audit = pd.DataFrame(columns=["level", "message"])

        
    # ---------------------------------------------------------------------------
    
    """
    Transformuje naskenovaný Excel blok do normalizovaného formátu.
    v2: okrem týždňov (WEEK) podporuje aj MONTH / QUARTER / HALF, ak sú v headers.

    Očakávané štruktúry v block["headers"]:
      - "static": {"Metric": <col_idx>}
      - "weeks":   [{"col": <int>, "label": "W1"}, ...]                (voliteľné)
      - "months":  [{"col": <int>, "label": "Jan"|"2025-01"}, ...]     (voliteľné)
      - "quarters":[{"col": <int>, "label": "Q1"|"2025-Q1"}, ...]      (voliteľné)
      - "halves":  [{"col": <int>, "label": "H1"|"2025-H1"}, ...]      (voliteľné)
    """
    rows = []
    audit_rows = []

    # --- Meta
    meta = block.get("meta", {}) or {}
    country = meta.get("country_hint", "UNKNOWN")
    business = meta.get("business_hint", "UNKNOWN")
    block_id = meta.get("block_id", "NA")

    # --- Headers
    headers = block.get("headers", {}) or {}
    metrics_col = (headers.get("static") or {}).get("Metric")

    # Priprav zoznam period setov, ktoré sú prítomné
    period_sets = []
    if headers.get("weeks"):
        period_sets.append(("WEEK", headers["weeks"]))
    if headers.get("months"):
        period_sets.append(("MONTH", headers["months"]))
    if headers.get("quarters"):
        period_sets.append(("QUARTER", headers["quarters"]))
    if headers.get("halves"):
        period_sets.append(("HALF", headers["halves"]))

    # --- Preindexuj bunky pre rýchly prístup (row,col) -> value
    cell_map = {}
    for c in block.get("cells", []) or []:
        cell_map[(c["row"], c["col"])] = c.get("value", None)

    # --- Prejdi riadky, kde je definovaná metrika
    for cell in block.get("cells", []) or []:
        if metrics_col and cell.get("col") == metrics_col:
            metric_name = str(cell.get("value", "")).strip()
            row_id = cell.get("row")

            for period_type, items in period_sets:
                for item in items:
                    col_idx = item["col"]
                    label = item["label"]  # Period (napr. "W1", "2025-01", "Q3", "H2")
                    raw = cell_map.get((row_id, col_idx), None)

                    quality = "OK"
                    notes = ""
                    value = None

                    if raw in (None, "", "-", "NaN"):
                        value = None
                        quality = "MISSING"
                    else:
                        try:
                            value = float(raw)
                        except Exception:
                            value = None
                            quality = "MISSING"
                            notes = "non-numeric"
                            audit_rows.append({
                                "level": "WARN",
                                "block_id": block_id,
                                "metric": metric_name,
                                "period": label,
                                "detail": f"Non-numeric value: {raw}",
                            })

                    rows.append({
                        "Country": country,
                        "Business": business,
                        "Metric": metric_name,
                        "PeriodType": period_type,
                        "Period": label,          # v2: ponechávame label tak, ako prišlo (bez ďalšej normalizácie)
                        "PeriodKey": _normalize_period(period_type, label, meta.get("year") or meta.get("year_hint")),
                        "Value": value,
                        "SourceBlockID": block_id,
                        "QualityFlag": quality,
                        "Notes": notes,
                    })

    data = pd.DataFrame(rows)
    audit = pd.DataFrame(audit_rows)
    return data, audit