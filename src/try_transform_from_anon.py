import argparse
from pathlib import Path
from transform import transform_block  # prispôsob ak má iný import
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Try transform from anonymized Excels.")
    parser.add_argument(
        "--in", dest="in_dir", required=True, help="Input folder with anonymized Excels"
    )
    parser.add_argument("--out", dest="out_dir", required=True, help="Output folder for CSVs")
    parser.add_argument("--log", dest="log_path", required=False, help="Optional log file path")
    args = parser.parse_args()

    in_dir = Path(args.in_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    all_results = []

    for f in in_dir.glob("*.xlsx"):
        print(f"→ Transforming {f.name}")
    # nahraď týmito 3 riadkami:
    res = transform_block(f)  # môže vrátiť df alebo (df, meta)
    df = res[0] if isinstance(res, tuple) else res
    df["source_file"] = f.name
    # ADAPTER: mapuj výstup s PeriodType/PeriodKey na facts (country, week, metric, value)
    need = {"Country", "Metric", "PeriodType", "PeriodKey", "Value"}
    if need.issubset(df.columns):
        # len týždne
        wk = (
            df.loc[df["PeriodType"] == "WEEK", "PeriodKey"]
            .astype("string")
            .str.extract(r"(\d{4})-W(\d{1,2})", expand=True)
        )
        df = df[df["PeriodType"] == "WEEK"].copy()
        df["week"] = pd.to_numeric(wk[1], errors="coerce").astype("Int64")

        # premenuj/typy
        df["country"] = df["Country"].astype("string")
        df["metric"] = df["Metric"].astype("string")
        df["value"] = pd.to_numeric(df["Value"], errors="coerce")

        if "Business" in df.columns:
            df["business"] = df["Business"].astype("string")

        cols = ["country", "week", "metric", "value"]
        if "business" in df.columns:
            cols.append("business")
        if "source_file" in df.columns:
            cols.append("source_file")
        df = df[cols]
    all_results.append(df)

    if all_results:
        result = pd.concat(all_results, ignore_index=True)
        out_path = out_dir / "facts.csv"
        result.to_csv(out_path, index=False)
        print(f"✔ Saved: {out_path}")
    else:
        print("⚠️ No Excel files found in input directory.")


if __name__ == "__main__":
    main()
