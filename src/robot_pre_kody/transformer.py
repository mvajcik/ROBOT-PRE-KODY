def extract_headers(block):
    """Identify week/month/quarter/half columns."""
    import re

    week_cols = []
    for col in block.columns:
        # match W1, W01, W12, Week 1, Week 12, etc.
        m = re.match(r"^(W|Week\s*)(\d{1,2})$", str(col))
        if m:
            week_num = int(m.group(2))
            week_cols.append(("week", week_num, col))

    return {"weeks": week_cols, "months": [], "quarters": [], "halves": []}


def normalize_cells(block):
    """Apply basic cleanup and normalization."""
    # For now, return the block unchanged; real fixes will be added later.
    return block


def melt_to_long(block):
    """Convert normalized block to long format."""
    import pandas as pd

    rows = []
    for r_idx, row in block.iterrows():
        for col in block.columns:
            rows.append({"row": r_idx, "column": col, "value": row[col]})

    return pd.DataFrame(rows)


def attach_meta(df, *, country, period, metric):
    """Add (Country, Week, Metric, Value, meta)."""
    import pandas as pd

    return pd.DataFrame(
        {
            "Country": country,
            "Week": [None] * len(df),
            "Metric": metric,
            "Value": df["value"],
            "meta": [{} for _ in range(len(df))],
        }
    )


def transform_block(block, *, country, metric):
    """Pipeline: headers → normalize → melt → meta."""
    headers = extract_headers(block)
    cleaned = normalize_cells(block)
    long_df = melt_to_long(cleaned)
    return attach_meta(long_df, country=country, period=headers, metric=metric)
